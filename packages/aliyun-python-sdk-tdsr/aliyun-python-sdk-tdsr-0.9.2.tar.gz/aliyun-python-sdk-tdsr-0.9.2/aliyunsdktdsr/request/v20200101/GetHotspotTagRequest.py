# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdktdsr.endpoint import endpoint_data

class GetHotspotTagRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'tdsr', '2020-01-01', 'GetHotspotTag')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_SubSceneUuid(self):
		return self.get_query_params().get('SubSceneUuid')

	def set_SubSceneUuid(self,SubSceneUuid):
		self.add_query_param('SubSceneUuid',SubSceneUuid)

	def get_Type(self):
		return self.get_query_params().get('Type')

	def set_Type(self,Type):
		self.add_query_param('Type',Type)

	def get_PreviewToken(self):
		return self.get_query_params().get('PreviewToken')

	def set_PreviewToken(self,PreviewToken):
		self.add_query_param('PreviewToken',PreviewToken)