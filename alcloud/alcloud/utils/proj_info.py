'''
ProjInfo class will query from the SQL and
store the specified params for model training and
AL algorithms.
'''

from ..config import SQL_proj_data_status_args, SQL_proj_settings_args

class ProjInfo:
    '''Information of project info for AL (query from sql)

    :param project_id: str
        Project id.

    :param type: {'model', 'al'}
        Where to use the instance.
    '''
    def __init__(self, project_id, type):
        pass

    def get_y_shape(self):
        pass

    def get_X_shape(self):
        pass

    def get_label_type(self):
        pass

    def get_model(self):
        '''Init a model object'''
        pass

    def get_qs_param(self):
        return dict()

    def get_model_param(self):
        return dict()

    def get_metric(self):
        pass

    @property
    def need_test(self):
        return False

    # lazy import
    def fetch_hierarchy_info(self):
        # fetch hierachy info
        # set a flag
        self._hierachy_info = True

    def get_budget(self):
        if not self._hierachy_info:
            self.fetch_hierarchy_info()

    def get_label_tree(self):
        """
        Return
        ------
        label_tree: 2D array
            The hierarchical relationships among data features.
            if node_i is the parent of node_j , then label_tree(i,j)=1
        """
        if not self._hierachy_info:
            self.fetch_hierarchy_info()

    def get_hierarchy_costs(self):
        if not self._hierachy_info:
            self.fetch_hierarchy_info()


class DataInfo:
    """

    """
    def __init__(self, project_id):
        pass

    def get_labeled_indexes(self):
        pass

    def get_labeled_set(self):
        return indexes, label

    def get_initial_labeled_indexes(self):
        pass

    def get_queried_indexes(self):
        pass

    def get_latest_labeled_indexes(self):
        pass

    def get_unlabeled_indexes(self):
        pass

    def set_labeled_status(self, indexes):
        pass

