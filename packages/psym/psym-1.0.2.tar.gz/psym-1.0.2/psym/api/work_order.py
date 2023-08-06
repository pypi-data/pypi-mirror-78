#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from psym.client import SymphonyClient
from psym.common.data_class import WorkOrder, WorkOrderType

from ..graphql.input.add_work_order import AddWorkOrderInput
from ..graphql.mutation.add_work_order import AddWorkOrderMutation


def add_work_order(
    client: SymphonyClient, name: str, work_order_type: WorkOrderType
) -> WorkOrder:
    """This function creates work order of with the given name and type

    Args:
        name (str): work order name
        work_order_type (`psym.common.data_class.WorkOrderType`): work order type

    Returns:
        `psym.common.data_class.WorkOrder`

    Example:
        ```
        work_order_type = client.add_work_order_type("Deployment work order")
        client.add_work_order_type("new work order", work_order_type)
        ```
    """
    result = AddWorkOrderMutation.execute(
        client,
        AddWorkOrderInput(
            name=name,
            workOrderTypeId=work_order_type.id,
            properties=[],
            checkList=[],
            checkListCategories=[],
        ),
    )
    return WorkOrder(id=result.id, name=result.name)
