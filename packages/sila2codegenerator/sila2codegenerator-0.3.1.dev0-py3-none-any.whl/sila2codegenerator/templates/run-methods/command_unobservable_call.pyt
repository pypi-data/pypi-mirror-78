def ${command_id}(self,
                  parameter: ${feature_identifier}_pb2.${command_id}_Parameters = None) \
        -> ${feature_identifier}_pb2.${command_id}_Responses:
    """
    Wrapper to call the unobservable command ${command_id} on the server.

    :param parameter: The parameter gRPC construct required for this command.

    :returns: A gRPC object with the response that has been defined for this command.
    """
    # noinspection PyUnusedLocal - type definition, just for convenience
    grpc_err: grpc.Call

    logging.debug("Calling ${command_id}:")
    try:
        # resolve to default if no value given
        #   TODO: Implement a more reasonable default value
        if parameter is None:
            parameter = ${feature_identifier}_pb2.${command_id}_Parameters(
                **${feature_identifier}_default_dict['${command_id}_Parameters']
            )

        response = self.${feature_identifier}_stub.${command_id}(parameter)

        logging.debug('${command_id} response: {response}'.format(response=response))
    except grpc.RpcError as grpc_err:
        self.grpc_error_handling(grpc_err)
        return None

    return response
