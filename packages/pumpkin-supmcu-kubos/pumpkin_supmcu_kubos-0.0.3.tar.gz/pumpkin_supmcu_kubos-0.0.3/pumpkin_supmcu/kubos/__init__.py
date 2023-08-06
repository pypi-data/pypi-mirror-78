# coding: utf-8
# ##############################################################################
#  (C) Copyright 2019 Pumpkin, Inc. All Rights Reserved.                       #
#                                                                              #
#  This file may be distributed under the terms of the License                 #
#  Agreement provided with this software.                                      #
#                                                                              #
#  THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,                   #
#  INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND                       #
#  FITNESS FOR A PARTICULAR PURPOSE.                                           #
# ##############################################################################
"""
The `pumpkin_supmcu.kubos` module contains an implementations of the :class:`~pumpkin_supmcu.i2c.I2CMaster` for the following
devices:

* The `KubOS I2C HAL <https://github.com/kubos/kubos/tree/master/hal/python-hal>`_ as :class:`~pumpkin_supmcu.kubos.I2CKubosMaster`.
"""
from .kubos import I2CKubosMaster
