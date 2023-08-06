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

    # initialise the return value
    return_value = None

    # TODO:
    #   Add implementation of ${implementation_mode} for command ${command_id} here and write the resulting response
    #   in return_value

    # fallback to default
    if return_value is None:
        return_value = ${feature_identifier}_pb2.${command_id}_Responses(
            **default_dict['${command_id}_Responses']
        )

    return return_value
