from datetime import datetime

from psrdb.graphql_table import GraphQLTable


class Observation(GraphQLTable):
    """Class for interacting with the Observation database object.

    Parameters
    ----------
    client : GraphQLClient
        GraphQLClient class instance with the URL and Token already set.
    """
    def __init__(self, client, logger=None):
        GraphQLTable.__init__(self, client, logger)
        self.table_name = "observation"
        self.field_names = [
            "id",
            "pulsar { name }",
            "calibration { id }",
            "calibration { location }",
            "telescope { name }",
            "project { code }",
            "project { short }",
            "utcStart",
            "beam",
            "band",
            "duration",
        ]

    def list(
        self,
        id=None,
        pulsar_name=None,
        telescope_name=None,
        project_id=None,
        project_short=None,
        utcs=None,
        utce=None,
        obs_type='fold',
    ):
        """Return a list of Observation information based on the `self.field_names` and filtered by the parameters.

        Parameters
        ----------
        id : int, optional
            Filter by the database ID, by default None
        pulsar_name : str, optional
            Filter by the pulsar name, by default None
        telescope_name : str, optional
            Filter by the telescope name, by default None
        project_id : int, optional
            Filter by the project id, by default None
        project_short : str, optional
            Filter by the project short name, by default None
        utcs : str, optional
            Filter by the utc start time greater than or equal to the timestamp in the format YYYY-MM-DDTHH:MM:SS+00:00, by default None
        utce : str, optional
            Filter by the utc start time less than or equal to the timestamp in the format YYYY-MM-DDTHH:MM:SS+00:00, by default None
        obs_type : str, optional
            Filter by the observation type (fold, search or cal), by default 'fold'

        Returns
        -------
        list of dicts
            If `self.get_dicts` is `True`, a list of dictionaries containing the results.
        client_response:
            Else a client response object.
        """
        # Convert dates to correct format
        if utcs == "":
            utcs = None
        elif utcs is not None:
            d = datetime.strptime(utcs, '%Y-%m-%d-%H:%M:%S')
            utcs = f"{d.date()}T{d.time()}+00:00"
        if utce == "":
            utce = None
        elif utce is not None:
            d = datetime.strptime(utce, '%Y-%m-%d-%H:%M:%S')
            utce = f"{d.date()}T{d.time()}+00:00"
        if project_short == "":
            project_short = None
        if pulsar_name == "":
            pulsar_name = None
        """Return a list of records matching the id and/or any of the arguments."""
        filters = [
            {"field": "id", "value": id},
            {"field": "pulsar_Name", "value": pulsar_name},
            {"field": "telescope_Name", "value": telescope_name},
            {"field": "project_Id", "value": project_id},
            {"field": "project_Short", "value": project_short},
            {"field": "utcStartGte", "value": utcs},
            {"field": "utcStartLte", "value": utce},
            {"field": "obsType", "value": obs_type},
        ]
        return GraphQLTable.list_graphql(self, self.table_name, filters, [], self.field_names)

    def create(
        self,
        pulsarName,
        telescopeName,
        projectCode,
        calibrationId,
        ephemerisText,
        frequency,
        bandwidth,
        nchan,
        beam,
        nant,
        nantEff,
        npol,
        obsType,
        utcStart,
        raj,
        decj,
        duration,
        nbit,
        tsamp,
        foldNbin,
        foldNchan,
        foldTsubint,
        filterbankNbit,
        filterbankNpol,
        filterbankNchan,
        filterbankTsamp,
        filterbankDm,
    ):
        """Create a new Observation database object.

        Parameters
        ----------
        pulsarName : str
            The pulsar name.
        telescopeName : str
            The telescope name.
        projectCode : str
            The project code.
        calibrationId : int
            The ID of the Calibration database object.
        ephemerisText : str
            The ephemeris text as a single string (includes new line characters).
        frequency : float
            The frequency of the observation in MHz.
        bandwidth : float
            The bandwidth of the observation in MHz.
        nchan : int
            The number of frequency channels.
        beam : int
            The beam number.
        nant : int
            The number of antennas used in the observation.
        nantEff : int
            The effective number of antennas used in the observation.
        npol : int
            The number of polarisations.
        obsType : str
            The type of observation (fold, search or cal).
        utcStart : `datetime`
            The UTC start time of the observation as a `datetime` object.
        raj : str
            The right ascension of the observation in HH:MM:SS.SS format.
        decj : str
            The declination of the observation in DD:MM:SS.SS format.
        duration : float
            The duration of the observation in seconds.
        nbit : int
            The number of bits per sample.
        tsamp : float
            The sampling time in microseconds.
        foldNbin : int
            The number of bins in the folded data (None for non fold observations).
        foldNchan : int
            The number of frequency channels in the folded data (None for non fold observations).
        foldTsubint : int
            The number of time samples in each sub-integration of the folded data (None for non fold observations).
        filterbankNbit : int
            The number of bits per sample in the filterbank data (None for non search observations).
        filterbankNpol : int
            The number of polarisations in the filterbank data (None for non search observations).
        filterbankNchan : int
            The number of frequency channels in the filterbank data (None for non search observations).
        filterbankTsamp : float
            The sampling time in microseconds in the filterbank data (None for non search observations).
        filterbankDm : float
            The dispersion measure in the filterbank data (None for non search observations).

        Returns
        -------
        client_response:
            A client response object.
        """
        # create a new record
        self.mutation_name = "createObservation"
        self.mutation = """
        mutation (
            $pulsarName: String!,
            $telescopeName: String!,
            $projectCode: String!,
            $calibrationId: Int!,
            $frequency: Float!,
            $bandwidth: Float!,
            $nchan: Int!,
            $beam: Int!,
            $nant: Int!,
            $nantEff: Int!,
            $npol: Int!,
            $obsType: String!,
            $utcStart: DateTime!,
            $raj: String!,
            $decj: String!,
            $duration: Float!,
            $nbit: Int!,
            $tsamp: Float!,
            # Fold options
            $ephemerisText: String,
            $foldNbin: Int,
            $foldNchan: Int,
            $foldTsubint: Int,
            # Search options
            $filterbankNbit: Int,
            $filterbankNpol: Int,
            $filterbankNchan: Int,
            $filterbankTsamp: Float,
            $filterbankDm: Float,
        ) {
            createObservation(input: {
                pulsarName: $pulsarName,
                telescopeName: $telescopeName,
                projectCode: $projectCode,
                calibrationId: $calibrationId,
                frequency: $frequency,
                bandwidth: $bandwidth,
                nchan: $nchan,
                beam: $beam,
                nant: $nant,
                nantEff: $nantEff,
                npol: $npol,
                obsType: $obsType,
                utcStart: $utcStart,
                raj: $raj,
                decj: $decj,
                duration: $duration,
                nbit: $nbit,
                tsamp: $tsamp,
                ephemerisText: $ephemerisText,
                foldNbin: $foldNbin,
                foldNchan: $foldNchan,
                foldTsubint: $foldTsubint,
                filterbankNbit: $filterbankNbit,
                filterbankNpol: $filterbankNpol,
                filterbankNchan: $filterbankNchan,
                filterbankTsamp: $filterbankTsamp,
                filterbankDm: $filterbankDm,
            }) {
                observation {
                    id
                }
            }
        }
        """
        self.variables = {
            "pulsarName": pulsarName,
            "telescopeName": telescopeName,
            "projectCode": projectCode,
            "calibrationId": calibrationId,
            "ephemerisText": ephemerisText,
            "frequency": frequency,
            "bandwidth": bandwidth,
            "nchan": nchan,
            "beam": beam,
            "nant": nant,
            "nantEff": nantEff,
            "npol": npol,
            "obsType": obsType,
            "utcStart": utcStart,
            "raj": raj,
            "decj": decj,
            "duration": duration,
            "nbit": nbit,
            "tsamp": tsamp,
            "foldNbin": foldNbin,
            "foldNchan": foldNchan,
            "foldTsubint": foldTsubint,
            "filterbankNbit": filterbankNbit,
            "filterbankNpol": filterbankNpol,
            "filterbankNchan": filterbankNchan,
            "filterbankTsamp": filterbankTsamp,
            "filterbankDm": filterbankDm,
        }
        return self.mutation_graphql()

    def update(
        self,
        id,
        pulsarName,
        telescopeName,
        projectCode,
        calibrationId,
        ephemerisText,
        frequency,
        bandwidth,
        nchan,
        beam,
        nant,
        nantEff,
        npol,
        obsType,
        utcStart,
        raj,
        decj,
        duration,
        nbit,
        tsamp,
        foldNbin,
        foldNchan,
        foldTsubint,
        filterbankNbit,
        filterbankNpol,
        filterbankNchan,
        filterbankTsamp,
        filterbankDm,
    ):
        """Update a Observation database object.

        Parameters
        ----------
        id : int
            The database ID
        pulsarName : str
            The pulsar name.
        telescopeName : str
            The telescope name.
        projectCode : str
            The project code.
        calibrationId : int
            The ID of the Calibration database object.
        ephemerisText : str
            The ephemeris text as a single string (includes new line characters).
        frequency : float
            The frequency of the observation in MHz.
        bandwidth : float
            The bandwidth of the observation in MHz.
        nchan : int
            The number of frequency channels.
        beam : int
            The beam number.
        nant : int
            The number of antennas used in the observation.
        nantEff : int
            The effective number of antennas used in the observation.
        npol : int
            The number of polarisations.
        obsType : str
            The type of observation (fold, search or cal).
        utcStart : `datetime`
            The UTC start time of the observation as a `datetime` object.
        raj : str
            The right ascension of the observation in HH:MM:SS.SS format.
        decj : str
            The declination of the observation in DD:MM:SS.SS format.
        duration : float
            The duration of the observation in seconds.
        nbit : int
            The number of bits per sample.
        tsamp : float
            The sampling time in microseconds.
        foldNbin : int
            The number of bins in the folded data (None for non fold observations).
        foldNchan : int
            The number of frequency channels in the folded data (None for non fold observations).
        foldTsubint : int
            The number of time samples in each sub-integration of the folded data (None for non fold observations).
        filterbankNbit : int
            The number of bits per sample in the filterbank data (None for non search observations).
        filterbankNpol : int
            The number of polarisations in the filterbank data (None for non search observations).
        filterbankNchan : int
            The number of frequency channels in the filterbank data (None for non search observations).
        filterbankTsamp : float
            The sampling time in microseconds in the filterbank data (None for non search observations).
        filterbankDm : float
            The dispersion measure in the filterbank data (None for non search observations).


        Returns
        -------
        client_response:
            A client response object.
        """
        self.mutation_name = "updateObservation"
        self.mutation = """
        mutation (
            $id: Int!,
            $pulsarName: String!,
            $telescopeName: String!,
            $projectCode: String!,
            $calibrationId: Int!,
            $frequency: Float!,
            $bandwidth: Float!,
            $nchan: Int!,
            $beam: Int!,
            $nant: Int!,
            $nantEff: Int!,
            $npol: Int!,
            $obsType: String!,
            $utcStart: DateTime!,
            $raj: String!,
            $decj: String!,
            $duration: Float!,
            $nbit: Int!,
            $tsamp: Float!,
            # Fold options
            $ephemerisText: String,
            $foldNbin: Int,
            $foldNchan: Int,
            $foldTsubint: Int,
            # Search options
            $filterbankNbit: Int,
            $filterbankNpol: Int,
            $filterbankNchan: Int,
            $filterbankTsamp: Float,
            $filterbankDm: Float,
        ) {
            updateObservation(input: {
                id: $id,
                pulsarName: $pulsarName,
                telescopeName: $telescopeName,
                projectCode: $projectCode,
                calibrationId: $calibrationId,
                frequency: $frequency,
                bandwidth: $bandwidth,
                nchan: $nchan,
                beam: $beam,
                nant: $nant,
                nantEff: $nantEff,
                npol: $npol,
                obsType: $obsType,
                utcStart: $utcStart,
                raj: $raj,
                decj: $decj,
                duration: $duration,
                nbit: $nbit,
                tsamp: $tsamp,
                ephemerisText: $ephemerisText,
                foldNbin: $foldNbin,
                foldNchan: $foldNchan,
                foldTsubint: $foldTsubint,
                filterbankNbit: $filterbankNbit,
                filterbankNpol: $filterbankNpol,
                filterbankNchan: $filterbankNchan,
                filterbankTsamp: $filterbankTsamp,
                filterbankDm: $filterbankDm,
            }) {
                observation {
                    id
                }
            }
        }
        """
        self.variables = {
            "id": id,
            "pulsarName": pulsarName,
            "telescopeName": telescopeName,
            "projectCode": projectCode,
            "calibrationId": calibrationId,
            "ephemerisText": ephemerisText,
            "frequency": frequency,
            "bandwidth": bandwidth,
            "nchan": nchan,
            "beam": beam,
            "nant": nant,
            "nantEff": nantEff,
            "npol": npol,
            "obsType": obsType,
            "utcStart": utcStart,
            "raj": raj,
            "decj": decj,
            "duration": duration,
            "nbit": nbit,
            "tsamp": tsamp,
            "foldNbin": foldNbin,
            "foldNchan": foldNchan,
            "foldTsubint": foldTsubint,
            "filterbankNbit": filterbankNbit,
            "filterbankNpol": filterbankNpol,
            "filterbankNchan": filterbankNchan,
            "filterbankTsamp": filterbankTsamp,
            "filterbankDm": filterbankDm,
        }
        return self.mutation_graphql()

    def delete(self, id):
        """Delete a Observation database object.

        Parameters
        ----------
        id : int
            The database ID

        Returns
        -------
        client_response:
            A client response object.
        """
        self.mutation_name = "deleteObservation"
        self.mutation = """
        mutation ($id: Int!) {
            deleteObservation(id: $id) {
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
            return self.create(
                args.target,
                args.calibration,
                args.telescope,
                args.instrument_config,
                args.project,
                args.config,
                args.utc,
                args.duration,
                args.nant,
                args.nanteff,
                args.suspect,
                args.comment,
            )
        elif args.subcommand == "update":
            return self.update(
                args.id,
                args.target,
                args.calibration,
                args.telescope,
                args.instrument_config,
                args.project,
                args.config,
                args.utc,
                args.duration,
                args.nant,
                args.nanteff,
                args.suspect,
                args.comment,
            )
        elif args.subcommand == "list":
            return self.list(
                id=args.id,
                pulsar_name=args.pulsar,
                telescope_name=args.telescope_name,
                project_id=args.project_id,
                project_short=args.project_code,
                utcs=args.utcs,
                utce=args.utce,
            )
        elif args.subcommand == "delete":
            return self.delete(args.id)
        else:
            raise RuntimeError(f"{args.subcommand} command is not implemented")

    @classmethod
    def get_name(cls):
        return "observation"

    @classmethod
    def get_description(cls):
        return "Observation details."

    @classmethod
    def get_parsers(cls):
        """Returns the default parser for this model"""
        parser = GraphQLTable.get_default_parser("Observations model parser")
        cls.configure_parsers(parser)
        return parser

    @classmethod
    def configure_parsers(cls, parser):
        """Add sub-parsers for each of the valid commands."""
        # create the parser for the "list" command
        parser.set_defaults(command=cls.get_name())
        subs = parser.add_subparsers(dest="subcommand")
        subs.required = True

        parser_list = subs.add_parser("list", help="list existing observations")
        parser_list.add_argument("--id", metavar="ID", type=int, help="list observations matching the id [int]")
        parser_list.add_argument(
            "--target_id", metavar="TGTID", type=int, help="list observations matching the target (pulsar) id [int]"
        )
        parser_list.add_argument(
            "--pulsar", metavar="TGTNAME", type=str, nargs='+', help="list observations matching the target (pulsar) name [str]"
        )
        parser_list.add_argument(
            "--telescope_id", metavar="TELID", type=int, help="list observations matching the telescope id [int]"
        )
        parser_list.add_argument(
            "--telescope_name", metavar="TELNAME", type=str, help="list observations matching the telescope name [int]"
        )
        parser_list.add_argument(
            "--instrumentconfig_id",
            metavar="ICID",
            type=int,
            help="list observations matching the instrument_config id [int]",
        )
        parser_list.add_argument(
            "--instrumentconfig_name",
            metavar="ICNAME",
            type=str,
            help="list observations matching the instrument_config name [str]",
        )
        parser_list.add_argument(
            "--project_id", metavar="PROJID", type=int, help="list observations matching the project id [id]"
        )
        parser_list.add_argument(
            "--project_code", metavar="PROJCODE", type=str, help="list observations matching the project code [str]"
        )
        parser_list.add_argument(
            "--utcs",
            metavar="UTCGTE",
            type=str,
            help="list observations with utc_start greater than or equal to the timestamp [YYYY-MM-DDTHH:MM:SS+HH:MM]",
        )
        parser_list.add_argument(
            "--utce",
            metavar="UTCLET",
            type=str,
            help="list observations with utc_start less than or equal to the timestamp [YYYY-MM-DDTHH:MM:SS+HH:MM]",
        )

        # create the parser for the "create" command
        parser_create = subs.add_parser("create", help="create a new observation")
        parser_create.add_argument("target", metavar="TGT", type=int, help="target id of the observation [int]")
        parser_create.add_argument(
            "calibration", metavar="CAL", type=int, help="calibration id of the observation [int]"
        )
        parser_create.add_argument("telescope", metavar="TEL", type=int, help="telescope id of the observation [int]")
        parser_create.add_argument(
            "instrument_config", metavar="IC", type=int, help="instrument config id of the observation [int]"
        )
        parser_create.add_argument("project", metavar="PROJ", type=int, help="project id of the observation [int]")
        parser_create.add_argument("config", metavar="CFG", type=str, help="json config of the observation [json]")
        parser_create.add_argument(
            "utc", metavar="UTC", type=str, help="start utc of the observation [YYYY-MM-DDTHH:MM:SS+00:00]"
        )
        parser_create.add_argument(
            "duration", metavar="DUR", type=float, help="duration of the observation in seconds [float]"
        )
        parser_create.add_argument(
            "nant", metavar="NANT", type=int, help="number of antennas used during the observation [int]"
        )
        parser_create.add_argument(
            "nanteff",
            metavar="NANTEFF",
            type=int,
            help="effective number of antennas used during the observation [int]",
        )
        parser_create.add_argument("suspect", metavar="SUS", type=bool, help="status of the observation [bool]")
        parser_create.add_argument("comment", metavar="COM", type=str, help="any comment on the observation [str]")

        parser_update = subs.add_parser("update", help="create a new observation")
        parser_update.add_argument("id", metavar="ID", type=int, help="id of the existing observation [int]")
        parser_update.add_argument("target", metavar="TGT", type=int, help="target id of the observation [int]")
        parser_update.add_argument(
            "calibration", metavar="CAL", type=int, help="calibration id of the observation [int]"
        )
        parser_update.add_argument("telescope", metavar="TEL", type=int, help="telescope id of the observation [int]")
        parser_update.add_argument(
            "instrument_config", metavar="IC", type=int, help="instrument config id of the observation [int]"
        )
        parser_update.add_argument("project", metavar="PROJ", type=int, help="project id of the observation [int]")
        parser_update.add_argument("config", metavar="CFG", type=str, help="json config of the observation [json]")
        parser_update.add_argument(
            "utc", metavar="UTC", type=str, help="start utc of the observation [YYYY-MM-DDTHH:MM:SS+00:00]"
        )
        parser_update.add_argument(
            "duration", metavar="DUR", type=float, help="duration of the observation in seconds [float]"
        )
        parser_update.add_argument(
            "nant", metavar="NANT", type=int, help="number of antennas used during the observation [int]"
        )
        parser_update.add_argument(
            "nanteff",
            metavar="NANTEFF",
            type=int,
            help="effective number of antennas used during the observation [int]",
        )
        parser_update.add_argument("suspect", metavar="SUS", type=bool, help="status of the observation [bool]")
        parser_update.add_argument("comment", metavar="COM", type=str, help="any comment on the observation [str]")

        # create the parser for the "delete" command
        parser_delete = subs.add_parser("delete", help="delete an existing observation")
        parser_delete.add_argument("id", metavar="ID", type=int, help="id of the existing observation [int]")

