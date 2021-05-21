import numpy as np
import xarray as xr
from liscal import calibration, utils


def test_phistory_ranked(dummy_cfg):

    path_subcatch = dummy_cfg.path_subcatch
    param_ranges = dummy_cfg.param_ranges
    path_result = dummy_cfg.path_result

    print('checking pHistory file')

    pHistory = calibration.read_param_history(path_subcatch)
    pHistory_ranked = calibration.write_ranked_solution(path_result, pHistory)

    ret, out = utils.run_cmd('diff {}/pHistoryWRanks.csv {}/pHistoryWRanks.csv'.format(path_subcatch, path_result))
    print(out)
    assert out == ''
    assert ret == 0


def test_pareto_front(dummy_cfg):
    path_subcatch = dummy_cfg.path_subcatch
    param_ranges = dummy_cfg.param_ranges
    path_result = dummy_cfg.path_result

    print('checking pareto_front file')

    pHistory = calibration.read_param_history(path_subcatch)
    pHistory_ranked = calibration.write_ranked_solution(path_subcatch, pHistory)
    calibration.write_pareto_front(param_ranges, path_result, pHistory_ranked)

    ret, out = utils.run_cmd('diff {}/pareto_front.csv {}/pareto_front.csv'.format(path_subcatch, path_result))
    print(out)
    assert out == ''
    assert ret == 0


def test_front_history(dummy_cfg):

    path_subcatch = dummy_cfg.path_subcatch
    path_result = dummy_cfg.path_result
    deap_param = dummy_cfg.deap_param

    print('checking front_history file')

    criteria = calibration.Criteria(deap_param)
    criteria.effmax = np.array([[0.9999384017071802], [0.9999384017071802]])
    criteria.effmin = np.array([[0.9999384017071802], [0.9999384017071802]])
    criteria.effstd = np.array([[0.0], [0.0]])
    criteria.effavg = np.array([[0.9999384017071802], [0.9999384017071802]])

    criteria.write_front_history(path_result, 2)

    ret, out = utils.run_cmd('diff {}/front_history.csv {}/front_history.csv'.format(path_subcatch, path_result))
    print(out)
    assert out == ''
    assert ret == 0

def test_termination_gen(dummy_cfg):

    path_subcatch = dummy_cfg.path_subcatch
    path_result = dummy_cfg.path_result
    deap_param = dummy_cfg.deap_param

    print('checking front_history file')

    criteria = calibration.Criteria(deap_param)
    criteria.gen_offset = 1

    assert criteria.conditions['maxGen'] == False
    assert criteria.conditions['StallFit'] == False

    gen = criteria.max_gen

    criteria.check_termination_conditions(gen)

    assert criteria.conditions['maxGen'] == True
    assert criteria.conditions['StallFit'] == False

def test_termination_gen(dummy_cfg):

    path_subcatch = dummy_cfg.path_subcatch
    path_result = dummy_cfg.path_result
    deap_param = dummy_cfg.deap_param

    criteria = calibration.Criteria(deap_param)
    print(criteria.effmax)
    criteria.gen_offset = 1

    assert criteria.conditions['maxGen'] == False
    assert criteria.conditions['StallFit'] == False

    gen = 1
    criteria.max_gen = 2
    criteria.effmax = np.array([[0.991], [0.991]])

    criteria.check_termination_conditions(gen)

    assert criteria.conditions['maxGen'] == False
    assert criteria.conditions['StallFit'] == True

def test_update(dummy_cfg):

    path_subcatch = dummy_cfg.path_subcatch
    path_result = dummy_cfg.path_result
    deap_param = dummy_cfg.deap_param

    criteria = calibration.Criteria(deap_param)
    criteria.effmax = np.array([[0.9999384017071802], [0.9999384017071802]])
    criteria.effmin = np.array([[0.9999384017071802], [0.9999384017071802]])
    criteria.effstd = np.array([[0.0], [0.0]])
    criteria.effavg = np.array([[0.9999384017071802], [0.9999384017071802]])
    
    halloffame = []
    ds1 = xr.Dataset()
    ds1['fitness'] = xr.DataArray(np.array([0.1]), dims=['x'])
    halloffame.append(ds1)
    ds2 = xr.Dataset()
    ds2['fitness'] = xr.DataArray(np.array([0.2]), dims=['x'])
    halloffame.append(ds2)
    
    gen = 1
    criteria.update_statistics(gen, halloffame)

    print(criteria.effmin[1, 0])
    assert criteria.effmin[1, 0] == 0.1
    print(criteria.effmax[1, 0])
    assert criteria.effmax[1, 0] == 0.2
    print(criteria.effstd[1, 0])
    assert criteria.effstd[1, 0] == 0.05
    print(criteria.effavg[1, 0])
    assert np.abs(criteria.effavg[1, 0] - 0.15) < 1e-8
