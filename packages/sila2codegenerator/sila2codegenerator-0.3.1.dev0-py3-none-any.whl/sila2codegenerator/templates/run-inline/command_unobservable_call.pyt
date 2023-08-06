logging.info(" " * 4 + "Calling ${command_id}:")
try:
    # value(s) to pass to the function
    value: ${feature_identifier}_pb2.${command_id}_Parameters = None

    # TODO:
    #   Implement actual value to pass

    # resolve to default if no value given
    if value is None:
        value = ${feature_identifier}_pb2.${command_id}_Parameters(
            **${feature_identifier}_default_dict['${command_id}_Parameters']
        )

    response = self.${feature_identifier}_stub.${command_id}(value)
    logging.debug(" " * 8 + '${command_id} response: {response}'.format(response=response))
except grpc.RpcError as grpc_err:
    logging.error(" " * 8 + "gRPC/SiLA error: {error}".format(error=grpc_err))
