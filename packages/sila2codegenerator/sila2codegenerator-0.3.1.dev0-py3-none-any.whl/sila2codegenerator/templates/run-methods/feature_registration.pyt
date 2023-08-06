#  Register ${feature_identifier}
self.${feature_identifier}_servicer = ${feature_identifier}(simulation_mode=self.simulation_mode)
${feature_identifier}_pb2_grpc.add_${feature_identifier}Servicer_to_server(
    self.${feature_identifier}_servicer,
    self.grpc_server
)
self.add_feature(feature_id='${feature_identifier}',
                 servicer=self.${feature_identifier}_servicer,
                 data_path='${meta_path}')