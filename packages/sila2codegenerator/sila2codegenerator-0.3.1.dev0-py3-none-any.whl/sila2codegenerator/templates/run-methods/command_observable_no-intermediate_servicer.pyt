def ${command_id}(self, request, context: grpc.ServicerContext) \
        -> ${sila_framework}.CommandConfirmation:
    """
    Executes the observable command "${command_name}"
${indent(8):trim(True,True):command_description}

    :param request: gRPC request containing the parameters passed:
${indent(8):trim(True,True):parameter_description}
    :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

    :returns: A command confirmation object with the following information:
        commandId: A command id with which this observable command can be referenced in future calls
        lifetimeOfExecution: The (maximum) lifetime of this command call.
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

def ${command_id}_Info(self, request, context: grpc.ServicerContext) \
        -> ${sila_framework}.ExecutionInfo:
    """
    Returns execution information regarding the command call :meth:`~.${command_id}`.

    :param request: A request object with the following properties
        CommandExecutionUUID: The UUID of the command executed.
    :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

    :returns: An ExecutionInfo response stream for the command with the following fields:
        commandStatus: Status of the command (enumeration)
        progressInfo: Information on the progress of the command (0 to 1)
        estimatedRemainingTime: Estimate of the remaining time required to run the command
        updatedLifetimeOfExecution: An update on the execution lifetime
    """

    logging.debug(
        "${command_id}_Info called in {current_mode} mode".format(
            current_mode=('simulation' if self.simulation_mode else 'real')
        )
    )
    try:
        return self.implementation.${command_id}_Info(request, context)
    except SiLAError as err:
        err.raise_rpc_error(context=context)

def ${command_id}_Result(self, request, context: grpc.ServicerContext) \
        -> ${feature_identifier}_pb2.${command_id}_Responses:
    """
    Returns the final result of the command call :meth:`~.${command_id}`.

    :param request: A request object with the following properties
        CommandExecutionUUID: The UUID of the command executed.
    :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

    :returns: The return object defined for the command with the following fields:
${indent(8):trim(True,True):response_description}
    """

    logging.debug(
        "${command_id}_Result called in {current_mode} mode".format(
            current_mode=('simulation' if self.simulation_mode else 'real')
        )
    )
    try:
        return self.implementation.${command_id}_Result(request, context)
    except SiLAError as err:
        err.raise_rpc_error(context=context)
