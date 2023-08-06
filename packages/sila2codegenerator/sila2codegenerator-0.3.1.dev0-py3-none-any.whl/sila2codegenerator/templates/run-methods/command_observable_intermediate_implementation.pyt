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

    # initialise default values
    #: Duration ${sila_framework}.Duration(seconds=<seconds>, nanos=<nanos>)
    lifetime_of_execution: ${sila_framework}.Duration = None

    # TODO:
    #   Execute the actual command in ${implementation_mode} mode
    #   Optional: Generate a lifetime_of_execution

    # respond with UUID and lifetime of execution
    command_uuid = ${sila_framework}.CommandExecutionUUID(value=str(uuid.uuid4()))
    if lifetime_of_execution is not None:
        return ${sila_framework}.CommandConfirmation(
            commandExecutionUUID=command_uuid,
            lifetimeOfExecution=lifetime_of_execution
        )
    else:
        return ${sila_framework}.CommandConfirmation(
            commandExecutionUUID=command_uuid
        )

def ${command_id}_Intermediate(self, request, context: grpc.ServicerContext) \
        -> ${feature_identifier}_pb2.${command_id}_IntermediateResponses:
    """
    Returns intermediate information on the command call :meth:`~.${command_id}`.

    :param request: A request object with the following properties
        CommandExecutionUUID: The UUID of the command executed.
    :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

    :returns: An intermediate response stream for the command with the following fields:
${indent(8):trim(True,True):intermediate_description}
    """

    # initialise the return value
    return_value: ${feature_identifier}_pb2.${command_id}_IntermediateResponses = None

    # Get the UUID of the command
    command_uuid = request.value

    # create a default response
    if return_value is None:
        return_value = ${feature_identifier}_pb2.${command_id}_IntermediateResponses(
            **default_dict['${command_id}_IntermediateResponses']
        )

    # consider some other way to break the loop
    command_status = self._get_command_state(command_uuid=command_uuid).commandStatus
    while command_status == ${sila_framework}.ExecutionInfo.CommandStatus.waiting \
            or command_status == ${sila_framework}.ExecutionInfo.CommandStatus.running:

        # TODO:
        #   Add implementation of ${implementation_mode} for command ${command_id} here and write the resulting intermediate
        #   response in return_value

        yield return_value

        # we add a small delay to give the client a chance to keep up.
        time.sleep(0.5)
        # update the status
        command_status = self._get_command_state(command_uuid=command_uuid).commandStatus
    else:
        # when the loop breaks..
        yield return_value

def ${command_id}_Info(self, request, context: grpc.ServicerContext) \
        -> ${sila_framework}.ExecutionInfo:
    """
    Returns execution information regarding the command call :meth:`~.${command_id}`.

    :param request: A request object with the following properties
        CommandExecutionUUID: The UUID of the command executed.
    :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

    :returns: An ExecutionInfo response stream for the command with the following fields:
                * *commandStatus*: Status of the command (enumeration)
                * *progressInfo*: Information on the progress of the command (0 to 1)
                * *estimatedRemainingTime*: Estimate of the remaining time required to run the command
                * *updatedLifetimeOfExecution*: An update on the execution lifetime
    """
    # Get the UUID of the command
    command_uuid = request.value

    # Get the current state
    execution_info = self._get_command_state(command_uuid=command_uuid)

    # construct the initial return dictionary in case while is not executed
    return_values = {'commandStatus': execution_info.commandStatus}
    if execution_info.HasField('progressInfo'):
        return_values['progressInfo'] = execution_info.progressInfo
    if execution_info.HasField('estimatedRemainingTime'):
        return_values['estimatedRemainingTime'] = execution_info.estimatedRemainingTime
    if execution_info.HasField('updatedLifetimeOfExecution'):
        return_values['updatedLifetimeOfExecution'] = execution_info.updatedLifetimeOfExecution

    # we loop only as long as the command is running
    while execution_info.commandStatus == ${sila_framework}.ExecutionInfo.CommandStatus.waiting \
            or execution_info.commandStatus == ${sila_framework}.ExecutionInfo.CommandStatus.running:
        # TODO:
        #   Evaluate the command status --> command_status. Options:
        #       command_stats = ${sila_framework}.ExecutionInfo.CommandStatus.waiting
        #       command_stats = ${sila_framework}.ExecutionInfo.CommandStatus.running
        #       command_stats = ${sila_framework}.ExecutionInfo.CommandStatus.finishedSuccessfully
        #       command_stats = ${sila_framework}.ExecutionInfo.CommandStatus.finishedWithError
        #   Optional:
        #       * Determine the progress (progressInfo)
        #       * Determine the estimated remaining time
        #       * Update the Lifetime of execution

        # Update all values
        execution_info = self._get_command_state(command_uuid=command_uuid)

        # construct the return dictionary
        return_values = {'commandStatus': execution_info.commandStatus}
        if execution_info.HasField('progressInfo'):
            return_values['progressInfo'] = execution_info.progressInfo
        if execution_info.HasField('estimatedRemainingTime'):
            return_values['estimatedRemainingTime'] = execution_info.estimatedRemainingTime
        if execution_info.HasField('updatedLifetimeOfExecution'):
            return_values['updatedLifetimeOfExecution'] = execution_info.updatedLifetimeOfExecution

        yield ${sila_framework}.ExecutionInfo(**return_values)

        # we add a small delay to give the client a chance to keep up.
        time.sleep(0.5)
    else:
        # one last time yield the status
        yield ${sila_framework}.ExecutionInfo(**return_values)

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

    # initialise the return value
    return_value: ${feature_identifier}_pb2.${command_id}_Responses = None

    # Get the UUID of the command
    command_uuid = request.value

    # TODO:
    #   Add implementation of ${implementation_mode} for command ${command_id} here and write the resulting response
    #   in return_value

    # fallback to default
    if return_value is None:
        return_value = ${feature_identifier}_pb2.${command_id}_Responses(
            **default_dict['${command_id}_Responses']
        )

    return return_value
