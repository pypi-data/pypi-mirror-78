def ${command_id}(self,
                  parameter: ${feature_identifier}_pb2.${command_id}_Parameters = None) \
        -> ${sila_framework}.CommandConfirmation:
    """
    Wrapper to call the observable command ${command_id} on the server.

    :param parameter: The parameter gRPC construct required for this command.

    :returns: A command confirmation object with the following information:
        commandExecutionUUID: A command id with which this observable command can be referenced in future calls
        lifetimeOfExecution (optional): The (maximum) lifetime of this command call.
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

        logging.debug(
            '${command_id} confirmation: uuid={uuid}, lifetimeOfExecution={LOF}'.format(
                uuid=response.commandId,
                LOF=response.lifetimeOfExecution.seconds
            )
        )
    except grpc.RpcError as grpc_err:
        self.grpc_error_handling(grpc_err)
        return None

    return response

def ${command_id}_Intermediate(self,
                               uuid: Union[str, ${sila_framework}.CommandExecutionUUID]) \
        -> ${feature_identifier}_pb2.${command_id}_IntermediateResponses:
    """
    Wrapper to get an intermediate response for the observable command ${command_id} on the server.

    :param uuid: The UUID that has been returned with the first command call. Can be given as string or as the
                 corresponding SiLA2 gRPC object.

    :returns: A gRPC object with the intermediate response that has been defined for this command.
    """
    # noinspection PyUnusedLocal - type definition, just for convenience
    grpc_err: grpc.Call

    if type(uuid) is str:
        uuid = ${sila_framework}.CommandExecutionUUID(value=uuid)

    logging.debug(
        "Requesting intermediate response for command ${command_id} (UUID={uuid}):".format(
            uuid=uuid.value
        )
    )
    try:
        return self.${feature_identifier}_stub.${command_id}_Intermediate(uuid)
    except grpc.RpcError as grpc_err:
        self.grpc_error_handling(grpc_err)
        return None

def ${command_id}_Info(self,
                       uuid: Union[str, ${sila_framework}.CommandExecutionUUID]) \
        -> ${sila_framework}.ExecutionInfo:
    """
    Wrapper to get an intermediate response for the observable command ${command_id} on the server.

    :param uuid: The UUID that has been returned with the first command call. Can be given as string or as the
                 corresponding SiLA2 gRPC object.

    :returns: A gRPC object with the status information that has been defined for this command. The following fields
              are defined:
                * *commandStatus*: Status of the command (enumeration)
                * *progressInfo*: Information on the progress of the command (0 to 1)
                * *estimatedRemainingTime*: Estimate of the remaining time required to run the command
                * *updatedLifetimeOfExecution*: An update on the execution lifetime
    """
    # noinspection PyUnusedLocal - type definition, just for convenience
    grpc_err: grpc.Call

    if type(uuid) is str:
        uuid = ${sila_framework}.CommandExecutionUUID(value=uuid)

    logging.debug(
        "Requesting status information for command ${command_id} (UUID={uuid}):".format(
            uuid=uuid.value
        )
    )
    try:
        return self.${feature_identifier}_stub.${command_id}_Info(uuid)
    except grpc.RpcError as grpc_err:
        self.grpc_error_handling(grpc_err)
        return None

def ${command_id}_Result(self,
                         uuid: Union[str, ${sila_framework}.CommandExecutionUUID]) \
        -> ${feature_identifier}_pb2.${command_id}_Responses:
    """
    Wrapper to get an intermediate response for the observable command ${command_id} on the server.

    :param uuid: The UUID that has been returned with the first command call. Can be given as string or as the
                 corresponding SiLA2 gRPC object.

    :returns: A gRPC object with the result response that has been defined for this command.

    .. note:: Whether the result is available or not can and should be evaluated by calling the
              :meth:`${command_id}_Info` method of this call.
    """
    # noinspection PyUnusedLocal - type definition, just for convenience
    grpc_err: grpc.Call

    if type(uuid) is str:
        uuid = ${sila_framework}.CommandExecutionUUID(value=uuid)

    logging.debug(
        "Requesting status information for command ${command_id} (UUID={uuid}):".format(
            uuid=uuid.value
        )
    )
    try:
        response = self.${feature_identifier}_stub.${command_id}_Result(uuid)
        logging.debug('${command_id} result response: {response}'.format(response=response))
    except grpc.RpcError as grpc_err:
        self.grpc_error_handling(grpc_err)
        return None

    return response
