from psrdb.graphql_table import GraphQLTable


class Calibration(GraphQLTable):
    """Class for interacting with the Calibration database object.

    Parameters
    ----------
    client : GraphQLClient
        GraphQLClient class instance with the URL and Token already set.
    """
    def __init__(self, client):
        GraphQLTable.__init__(self, client)
        self.table_name = "calibration"
        self.field_names = ["id", "delayCalId", "phaseUpId", "calibrationType", "location"]

    def list(self, id=None, type=None):
        """Return a list of Calibration information based on the `self.field_names` and filtered by the parameters.

        Parameters
        ----------
        id : int, optional
            Filter by the database ID, by default None
        type : str, optional
            Filter by the observation type (pre or post), by default None

        Returns
        -------
        list of dicts
            If `self.get_dicts` is `True`, a list of dictionaries containing the results.
        client_response:
            Else a client response object.
        """
        filters = [
            {"field": "id", "value": id},
            {"field": "type", "value": type},
        ]
        return GraphQLTable.list_graphql(self, self.table_name, filters, [], self.field_names)

    def create(self, schedule_block_id, type, location):
        """Create a new Calibration database object.

        Parameters
        ----------
        schedule_block_id : str
            The schedule block ID which this calibration is associated with.
        type : str
            The type of calibration (pre or post).
        location : str
            The location of the calibration file on the filesystem (if a post type calibration).

        Returns
        -------
        client_response:
            A client response object.
        """
        self.mutation_name = "createCalibration"
        self.mutation = """
        mutation (
            $schedule_block_id: String,
            $calibration_type: String!,
            $location: String,
        ) {
            createCalibration(input: {
                scheduleBlockId: $schedule_block_id,
                calibrationType: $calibration_type,
                location: $location
                }) {
                calibration {
                    id
                }
            }
        }
        """
        self.variables = {
            "schedule_block_id": schedule_block_id,
            "calibration_type": type,
            "location": location,
        }
        return self.mutation_graphql()

    def update(self, id, schedule_block_id, type, location):
        """Update a Calibration database object.

        Parameters
        ----------
        id : int
            The database ID
        schedule_block_id : str
            The schedule block ID which this calibration is associated with.
        type : str
            The type of calibration (pre or post).
        location : str
            The location of the calibration file on the filesystem (if a post type calibration).

        Returns
        -------
        client_response:
            A client response object.
        """
        self.mutation_name = "updateCalibration"
        self.mutation = """
        mutation ($id: Int!, $calibration_type: String!, $location: String!) {
            updateCalibration(id: $id, input: {
                calibrationType: $calibration_type,
                location: $location
            }) {
                calibration {
                    id
                    calibrationType,
                    location
                }
            }
        }
        """
        self.variables = {
            "id": id,
            "schedule_block_id": schedule_block_id,
            "calibration_type": type,
            "location": location,
        }
        return self.mutation_graphql()

    def delete(self, id):
        """Delete a Calibration database object.

        Parameters
        ----------
        id : int
            The database ID

        Returns
        -------
        client_response:
            A client response object.
        """
        self.mutation_name = "deleteCalibration"
        self.mutation = """
        mutation ($id: Int!) {
            deleteCalibration(id: $id) {
                ok
            }
        }
        """
        self.variables = {
            "id": id,
        }
        return self.mutation_graphql()

    def process(self, args):
        """Parse the arguments collected by the CLI."""
        self.print_stdout = True
        if args.subcommand == "create":
            return self.create(args.delay_cal_id, args.type, args.location)
        elif args.subcommand == "list":
            return self.list(args.id, args.type)
        elif args.subcommand == "update":
            return self.update(args.id, args.type, args.location)
        elif args.subcommand == "delete":
            return self.delete(args.id)
        else:
            raise RuntimeError(f"{args.subcommand} command is not implemented")

    @classmethod
    def get_name(cls):
        return "calibration"

    @classmethod
    def get_description(cls):
        return "A defined by its type and location"

    @classmethod
    def get_parsers():
        """Returns the default parser for this model"""
        parser = GraphQLTable.get_default_parser("Calibration model parser")
        Calibration.configure_parsers(parser)
        return parser

    @classmethod
    def configure_parsers(cls, parser):
        """Add sub-parsers for each of the valid commands."""
        # create the parser for the "list" command
        parser.set_defaults(command=cls.get_name())
        subs = parser.add_subparsers(dest="subcommand")
        subs.required = True

        parser_list = subs.add_parser("list", help="list existing calibrations")
        parser_list.add_argument("--id", type=int, help="list calibrations matching the id [int]")
        parser_list.add_argument("--type", type=str, help="list calibrations matching the type [pre, post or none]")

        # create the parser for the "create" command
        parser_create = subs.add_parser("create", help="create a new calibration")
        parser_create.add_argument(
            "delay_cal_id", type=str, metavar="CALID", help="ID of the calibration (e.g. 20201022-0018) [str]"
        )
        parser_create.add_argument("type", type=str, metavar="TYPE", help="type of the calibration [pre, post, none]")
        parser_create.add_argument(
            "location", type=str, metavar="LOCATION", help="location of the calibration on the filesystem [str]"
        )

        parser_udpate = subs.add_parser("update", help="update the values of an existing calibration")
        parser_udpate.add_argument("id", type=int, metavar="ID", help="database id of the calibration [int]")
        parser_udpate.add_argument("type", type=str, metavar="TYPE", help="type of the calibration [pre, post, none]")
        parser_udpate.add_argument(
            "location", type=str, metavar="LOCATION", help="location of the calibration on the filesystem [int]"
        )

        # create the parser for the "delete" command
        parser_delete = subs.add_parser("delete", help="delete an existing calibration")
        parser_delete.add_argument("id", type=int, help="id of the calibration")

