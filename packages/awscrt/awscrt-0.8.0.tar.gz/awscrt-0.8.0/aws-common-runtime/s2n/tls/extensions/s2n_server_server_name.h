/*
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */

#pragma once

int s2n_server_extensions_server_name_send_size(struct s2n_connection *conn);
int s2n_server_extensions_server_name_send(struct s2n_connection *conn, struct s2n_stuffer *out);
int s2n_recv_server_server_name(struct s2n_connection *conn, struct s2n_stuffer *extension);
