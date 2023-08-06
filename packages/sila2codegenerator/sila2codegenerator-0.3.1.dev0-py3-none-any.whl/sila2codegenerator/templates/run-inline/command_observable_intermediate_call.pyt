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

    # start the observable command
    command_confirmation_response = self.${feature_identifier}_stub.${command_id}(value)
    commandUUID = command_confirmation_response.commandExecutionUUID
    # we define a timeout for the command either with a default (15 seconds) or by reading
    #   the lifetime of execution response from the server
    timeout = 15.0 if not command_confirmation_response.HasField("lifetimeOfExecution") \
        else command_confirmation_response.lifetimeOfExecution.seconds
    timeout = time.time() + timeout

    # repeatedly request information
    info_response = None
    for info_response in self.${feature_identifier}_stub.${command_id}_Info(commandUUID):
        # maybe we got more information? We might want to use this
        if info_response.HasField('progressInfo'):
            logging.info(
                'Running command ${command_id}, progress: {progress} %'.format(
                    progress=(info_response.progressInfo.value * 100)
                )
            )
        if info_response.HasField('estimatedRemainingTime'):
            logging.info(
                'Estimated remaining time: {remaining} s'.format(
                    remaining=info_response.estimatedRemainingTime.seconds
                )
            )
        if info_response.HasField('updatedLifetimeOfExecution') \
                and info_response.updatedLifetimeOfExecution.seconds < timeout - time.time():
            # lifetime is shorter, let's update our timeout
            timeout = time.time() + info_response.updatedLifetimeOfExecution.seconds

        # Let's have a look at the intermediate information we can receive
        for intermediate \
                in self.${feature_identifier}_stub.${command_id}_Intermediate(commandUUID):
            logging.info(
                'Intermediate response from command ${command_id}: {response}'.format(
                    response=intermediate
                )
            )
            break

        # check conditions to break the loop, note that the server can also close the loop
        #   by not yielding any more information responses
        if time.time() > timeout:
            break

        if info_response.commandStatus == ${sila_framework}.ExecutionInfo.CommandStatus.finishedSuccessfully:
            break

        if info_response.commandStatus == ${sila_framework}.ExecutionInfo.CommandStatus.finishedWithError:
            break

    if info_response is None:
        logging.error(
            'Could not get any information on the state of command ${command_id} (uuid={uuid})'.format(
                uuid=commandUUID.value
            )
        )
    elif info_response.commandStatus == ${sila_framework}.ExecutionInfo.CommandStatus.waiting \
            or info_response.commandStatus == ${sila_framework}.ExecutionInfo.CommandStatus.running:
        logging.exception(
            'Command ${command_id} (uuid={uuid}) did not finish before the timeout triggered.'.format(
                uuid=commandUUID.value
            )
        )
    elif info_response.commandStatus == ${sila_framework}.ExecutionInfo.CommandStatus.finishedSuccessfully:
        response = self.${feature_identifier}_stub.${command_id}_Result(commandUUID)
        logging.debug(
            " " * 8 + '${command_id} result: {response}'.format(
                response=response
            )
        )
    else:
        logging.exception('Command ${command_id} failed with an error!')

except grpc.RpcError as grpc_err:
    logging.error(" " * 8 + "gRPC/SiLA error: {error}".format(error=grpc_err))