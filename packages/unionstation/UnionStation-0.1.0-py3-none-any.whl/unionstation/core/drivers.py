# UnionStation -- the Data Work
# Copyright 2020 The UnionStation Author. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""UnionStation generic dataset driver class """

from typing import Generator

# from .aws_utils import S3Access


class Driver(object):
    """ iDataset static dataset driver """

    def __init__(self):
        # self.aws = S3Access(profile=meta.get('awsprofile', ""))
        self._pump_in()

    def _pump_in(self):
        """ Prepareing inet for dataset driver """
        pass

    def __len__(self):
        """ get the length of the dataset """
        return self.dataset_size

    def size(self):
        return self.__len__()

    def info(self):
        """ dataset meta data """
        pass

    def __getitem__(self, id):
        """ get dataset example by index """
        pass

    def driver(sefl) -> Generator:
        """ Returns a data serving generator """
        pass
