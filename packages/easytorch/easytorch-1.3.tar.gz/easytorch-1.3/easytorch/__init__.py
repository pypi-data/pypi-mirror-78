import json as _json
import os as _os

from easytorch.core import utils as _utils
from easytorch.utils import logutils as _logutils
from easytorch.utils.datautils import create_k_fold_splits as _create_splits

_sep = _os.sep


class EasyTorch:
    def __init__(self, args_parser, dataspecs):
        self.args = _utils.FrozenDict(vars(args_parser.parse_args()))
        self.dataspecs = dataspecs

    def _get_train_dataset(self, split, dspec, dataset_cls):
        train_dataset = dataset_cls(mode='train', limit=self.args['load_limit'])
        train_dataset.add(files=split['train'], debug=self.args['debug'], **dspec)
        return train_dataset

    def _get_validation_dataset(self, split, dspec, dataset_cls):
        val_dataset = dataset_cls(mode='eval', limit=self.args['load_limit'])
        val_dataset.add(files=split['validation'], debug=self.args['debug'], **dspec)
        return val_dataset

    def _get_test_dataset(self, split, dspec, dataset_cls):
        test_dataset_list = []
        if self.args.get('load_sparse'):
            for f in split['test']:
                if len(test_dataset_list) >= self.args['load_limit']:
                    break
                test_dataset = dataset_cls(mode='eval', limit=self.args['load_limit'])
                test_dataset.add(files=[f], debug=False, **dspec)
                test_dataset_list.append(test_dataset)
            if self.args['debug']:
                print(f'{len(test_dataset_list)} sparse dataset loaded.')
        else:
            test_dataset = dataset_cls(mode='eval', limit=self.args['load_limit'])
            test_dataset.add(files=split['test'], debug=self.args['debug'], **dspec)
            test_dataset_list.append(test_dataset)
        return test_dataset_list

    def _init_dataset(self, dspec, log_dir):
        for k in dspec:
            if 'dir' in k:
                dspec[k] = _os.path.join(self.args['dataset_dir'], dspec[k])

        if dspec.get('split_dir') and _os.path.exists(dspec.get('split_dir')) and len(list(
                _os.listdir(dspec.get('split_dir')))) > 0:
            return

        split_dir = log_dir + _sep + 'splits'
        _os.makedirs(split_dir, exist_ok=True)
        if not _os.path.exists(split_dir) or len(list(_os.listdir(split_dir))) <= 0:
            _create_splits(_os.listdir(dspec['data_dir']), k=self.args['num_folds'], save_to_dir=split_dir,
                           shuffle_files=True)
        dspec['split_dir'] = split_dir

    def run(self, dataset_cls, trainer_cls):
        for dspec in self.dataspecs:
            trainer = trainer_cls(self.args)
            global_score = trainer.new_metrics()

            trainer.cache['log_dir'] = self.args['log_dir'] + _sep + dspec['name']
            _os.makedirs(trainer.cache['log_dir'], exist_ok=True)

            self._init_dataset(dspec, log_dir=trainer.cache['log_dir'])

            trainer.reset_dataset_cache()
            for split_file in _os.listdir(dspec['split_dir']):
                split = _json.loads(open(dspec['split_dir'] + _sep + split_file).read())

                trainer.cache['experiment_id'] = split_file.split('.')[0]
                trainer.cache['checkpoint'] = trainer.cache['experiment_id'] + '.pt'
                trainer.cache.update(best_epoch=0, best_score=0.0)
                if trainer.cache['score_direction'] == 'minimize':
                    trainer.cache['best_score'] = 1e11

                trainer.check_previous_logs()
                trainer.init_nn()
                trainer.reset_fold_cache()

                """###########  Run training phase ########################"""
                if self.args['phase'] == 'train':
                    trainset = self._get_train_dataset(split, dspec, dataset_cls)
                    valset = self._get_validation_dataset(split, dspec, dataset_cls)
                    trainer.train(trainset, valset)
                    cache = {**self.args, **trainer.cache, **dspec, **trainer.nn, **trainer.optimizer}
                    _logutils.save_cache(cache, experiment_id=trainer.cache['experiment_id'])
                """#########################################################"""

                if self.args['phase'] == 'train' or self.args['pretrained_path'] is None:
                    trainer.load_best_model()

                """########## Run test phase. ##############################"""
                testset = self._get_test_dataset(split, dspec, dataset_cls)
                test_loss, test_score = trainer.evaluation(split_key='test', save_pred=True,
                                                           dataset_list=testset)
                global_score.accumulate(test_score)
                trainer.cache['test_score'].append([split_file] + test_score.scores())
                trainer.cache['global_test_score'].append([split_file] + test_score.scores())
                _logutils.save_scores(trainer.cache, experiment_id=trainer.cache['experiment_id'],
                                      file_keys=['test_score'])
                """#######################################################"""

            trainer.cache['global_test_score'].append(['Global'] + global_score.scores())
            _logutils.save_scores(trainer.cache, file_keys=['global_test_score'])

    def run_pooled(self, dataset_cls, trainer_cls):
        trainer = trainer_cls(self.args)
        trainer.cache['log_dir'] = self.args['log_dir'] + _sep + 'pooled'
        trainer.reset_dataset_cache()
        _os.makedirs(trainer.cache['log_dir'], exist_ok=True)

        trainer.cache['experiment_id'] = 'pooled'
        trainer.cache['checkpoint'] = trainer.cache['experiment_id'] + '.pt'

        global_score = trainer.new_metrics()
        trainer.cache.update(best_epoch=0, best_score=0.0)
        if trainer.cache['score_direction'] == 'minimize':
            trainer.cache['best_score'] = 10e10

        trainer.check_previous_logs()
        trainer.init_nn()
        trainer.reset_fold_cache()

        if self.args['phase'] == 'train':
            train_dataset = dataset_cls.pool(self.args, dataspecs=self.dataspecs, split_key='train',
                                             load_sparse=False)
            val_dataset = dataset_cls.pool(self.args, dataspecs=self.dataspecs, split_key='validation',
                                           load_sparse=False)
            trainer.train(train_dataset, val_dataset)
            cache = {**self.args, **trainer.cache, 'dataspecs': self.dataspecs}
            _logutils.save_cache(cache, experiment_id=cache['experiment_id'])

        if self.args['phase'] == 'train' or self.args['pretrained_path'] is None:
            trainer.load_best_model()

        test_dataset_list = dataset_cls.pool(self.args, dataspecs=self.dataspecs, split_key='test',
                                             load_sparse=self.args['load_sparse'])
        test_loss, test_score = trainer.evaluation(split_key='test', save_pred=True, dataset_list=test_dataset_list)
        global_score.accumulate(test_score)
        trainer.cache['test_score'].append(['Global'] + global_score.prfa())
        _logutils.save_scores(trainer.cache, experiment_id=trainer.cache['experiment_id'], file_keys=['test_score'])
