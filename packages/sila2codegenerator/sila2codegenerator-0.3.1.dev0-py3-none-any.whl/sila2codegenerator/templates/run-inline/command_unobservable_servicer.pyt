def ${command_id}(self, request, context: grpc.ServicerContext) \
        -> ${feature_identifier}_pb2.${command_id}_Responses:
    """
    Executes the unobservable command "${command_name}"
${indent(8):trim(True,True):command_description}

    :param request: gRPC request containing the parameters passed:
${indent(8):trim(True,True):parameter_description}
    :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

    :returns: The return object defined for the command with the following fields:
${indent(8):trim(True,True):response_description}
    """

    logging.debug(
        "${command_id} called in {current_mode} mode".format(
            current_mode=('simulation' if self.simulation_mode else 'real')
        )
    )

    try:
        return self.implementation.${command_id}(request, context)
    except SiLAError as err:
        err.raise_rpc_error(context=context)
