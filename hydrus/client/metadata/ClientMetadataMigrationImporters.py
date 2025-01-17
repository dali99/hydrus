import os
import typing

from hydrus.core import HydrusGlobals as HG
from hydrus.core import HydrusSerialisable
from hydrus.core import HydrusText

from hydrus.client import ClientConstants as CC
from hydrus.client import ClientParsing
from hydrus.client import ClientStrings
from hydrus.client.media import ClientMediaResult
from hydrus.client.metadata import ClientMetadataMigrationCore
from hydrus.client.metadata import ClientTags

# TODO: All importers should probably have a string processor

class SingleFileMetadataImporter( ClientMetadataMigrationCore.ImporterExporterNode ):
    
    def __init__( self, string_processor: ClientStrings.StringProcessor ):
        
        self._string_processor = string_processor
        
    
    def GetStringProcessor( self ) -> ClientStrings.StringProcessor:
        
        return self._string_processor
        
    
    def Import( self, *args, **kwargs ):
        
        raise NotImplementedError()
        
    
    def ToString( self ) -> str:
        
        raise NotImplementedError()
        
    

class SingleFileMetadataImporterMedia( SingleFileMetadataImporter ):
    
    def Import( self, media_result: ClientMediaResult.MediaResult ):
        
        raise NotImplementedError()
        
    
    def ToString( self ) -> str:
        
        raise NotImplementedError()
        
    

class SingleFileMetadataImporterSidecar( SingleFileMetadataImporter, ClientMetadataMigrationCore.SidecarNode ):
    
    def __init__( self, string_processor: ClientStrings.StringProcessor, remove_actual_filename_ext: bool, suffix: str, filename_string_converter: ClientStrings.StringConverter ):
        
        ClientMetadataMigrationCore.SidecarNode.__init__( self, remove_actual_filename_ext, suffix, filename_string_converter )
        SingleFileMetadataImporter.__init__( self, string_processor )
        
    
    def GetExpectedSidecarPath( self, path: str ):
        
        raise NotImplementedError()
        
    
    def Import( self, actual_file_path: str ):
        
        raise NotImplementedError()
        
    
    def ToString( self ) -> str:
        
        raise NotImplementedError()
        
    

class SingleFileMetadataImporterMediaTags( HydrusSerialisable.SerialisableBase, SingleFileMetadataImporterMedia ):
    
    SERIALISABLE_TYPE = HydrusSerialisable.SERIALISABLE_TYPE_METADATA_SINGLE_FILE_IMPORTER_MEDIA_TAGS
    SERIALISABLE_NAME = 'Metadata Single File Importer Media Tags'
    SERIALISABLE_VERSION = 2
    
    def __init__( self, string_processor = None, service_key = None ):
        
        if string_processor is None:
            
            string_processor = ClientStrings.StringProcessor()
            
        
        HydrusSerialisable.SerialisableBase.__init__( self )
        SingleFileMetadataImporterMedia.__init__( self, string_processor )
        
        if service_key is None:
            
            service_key = CC.COMBINED_TAG_SERVICE_KEY
            
        
        self._service_key = service_key
        
    
    def _GetSerialisableInfo( self ):
        
        serialisable_string_processor = self._string_processor.GetSerialisableTuple()
        serialisable_service_key = self._service_key.hex()
        
        return ( serialisable_string_processor, serialisable_service_key )
        
    
    def _InitialiseFromSerialisableInfo( self, serialisable_info ):
    
        ( serialisable_string_processor, serialisable_service_key ) = serialisable_info
        
        self._string_processor = HydrusSerialisable.CreateFromSerialisableTuple( serialisable_string_processor )
        self._service_key = bytes.fromhex( serialisable_service_key )
        
    
    def _UpdateSerialisableInfo( self, version, old_serialisable_info ):
        
        if version == 1:
            
            serialisable_service_key = old_serialisable_info
            
            string_processor = ClientStrings.StringProcessor()
            
            serialisable_string_processor = string_processor.GetSerialisableTuple()
            
            new_serialisable_info = ( serialisable_string_processor, serialisable_service_key )
            
            return ( 2, new_serialisable_info )
            
        
    
    def GetExampleStrings( self ):
        
        examples = [
            'blue eyes',
            'blonde hair',
            'skirt',
            'character:jane smith',
            'series:jane smith adventures',
            'creator:some guy'
        ]
        
        return examples
        
    
    def GetServiceKey( self ) -> bytes:
        
        return self._service_key
        
    
    def Import( self, media_result: ClientMediaResult.MediaResult ):
        
        tags = media_result.GetTagsManager().GetCurrent( self._service_key, ClientTags.TAG_DISPLAY_STORAGE )
        
        if self._string_processor.MakesChanges():
            
            tags = self._string_processor.ProcessStrings( tags )
            
        
        return tags
        
    
    def SetServiceKey( self, service_key: bytes ):
        
        self._service_key = service_key
        
    
    def ToString( self ) -> str:
        
        try:
            
            name = HG.client_controller.services_manager.GetName( self._service_key )
            
        except:
            
            name = 'unknown service'
            
        
        if self._string_processor.MakesChanges():
            
            full_munge_text = ', applying {}'.format( self._string_processor.ToString() )
            
        else:
            
            full_munge_text = ''
            
        
        return '"{}" tags from media{}'.format( name, full_munge_text )
        
    

HydrusSerialisable.SERIALISABLE_TYPES_TO_OBJECT_TYPES[ HydrusSerialisable.SERIALISABLE_TYPE_METADATA_SINGLE_FILE_IMPORTER_MEDIA_TAGS ] = SingleFileMetadataImporterMediaTags

class SingleFileMetadataImporterMediaURLs( HydrusSerialisable.SerialisableBase, SingleFileMetadataImporterMedia ):
    
    SERIALISABLE_TYPE = HydrusSerialisable.SERIALISABLE_TYPE_METADATA_SINGLE_FILE_IMPORTER_MEDIA_URLS
    SERIALISABLE_NAME = 'Metadata Single File Importer Media URLs'
    SERIALISABLE_VERSION = 2
    
    def __init__( self, string_processor = None ):
        
        if string_processor is None:
            
            string_processor = ClientStrings.StringProcessor()
            
        
        HydrusSerialisable.SerialisableBase.__init__( self )
        SingleFileMetadataImporterMedia.__init__( self, string_processor )
        
    
    def _GetSerialisableInfo( self ):
        
        serialisable_string_processor = self._string_processor.GetSerialisableTuple()
        
        return serialisable_string_processor
        
    
    def _InitialiseFromSerialisableInfo( self, serialisable_info ):
        
        serialisable_string_processor = serialisable_info
        
        self._string_processor = HydrusSerialisable.CreateFromSerialisableTuple( serialisable_string_processor )
        
    
    def _UpdateSerialisableInfo( self, version, old_serialisable_info ):
        
        if version == 1:
            
            gumpf = old_serialisable_info
            
            string_processor = ClientStrings.StringProcessor()
            
            serialisable_string_processor = string_processor.GetSerialisableTuple()
            
            new_serialisable_info = serialisable_string_processor
            
            return ( 2, new_serialisable_info )
            
        
    
    def GetExampleStrings( self ):
        
        examples = [
            'https://example.com/gallery/index.php?post=123456&page=show',
            'https://cdn3.expl.com/files/file_id?id=123456&token=0123456789abcdef'
        ]
        
        return examples
        
    
    def Import( self, media_result: ClientMediaResult.MediaResult ):
        
        urls = media_result.GetLocationsManager().GetURLs()
        
        if self._string_processor.MakesChanges():
            
            urls = self._string_processor.ProcessStrings( urls )
            
        
        return urls
        
    
    def ToString( self ) -> str:
        
        if self._string_processor.MakesChanges():
            
            full_munge_text = ', applying {}'.format( self._string_processor.ToString() )
            
        else:
            
            full_munge_text = ''
            
        
        return 'urls from media{}'.format( full_munge_text )
        
    

HydrusSerialisable.SERIALISABLE_TYPES_TO_OBJECT_TYPES[ HydrusSerialisable.SERIALISABLE_TYPE_METADATA_SINGLE_FILE_IMPORTER_MEDIA_URLS ] = SingleFileMetadataImporterMediaURLs

class SingleFileMetadataImporterJSON( HydrusSerialisable.SerialisableBase, SingleFileMetadataImporterSidecar ):
    
    SERIALISABLE_TYPE = HydrusSerialisable.SERIALISABLE_TYPE_METADATA_SINGLE_FILE_IMPORTER_JSON
    SERIALISABLE_NAME = 'Metadata Single File Importer JSON'
    SERIALISABLE_VERSION = 3
    
    def __init__( self, string_processor = None, remove_actual_filename_ext = None, suffix = None, filename_string_converter = None, json_parsing_formula = None ):
        
        if remove_actual_filename_ext is None:
            
            remove_actual_filename_ext = False
            
        
        if suffix is None:
            
            suffix = ''
            
        
        if filename_string_converter is None:
            
            filename_string_converter = ClientStrings.StringConverter( example_string = 'my_image.jpg.json' )
            
        
        if string_processor is None:
            
            string_processor = ClientStrings.StringProcessor()
            
        
        HydrusSerialisable.SerialisableBase.__init__( self )
        SingleFileMetadataImporterSidecar.__init__( self, string_processor, remove_actual_filename_ext, suffix, filename_string_converter )
        
        if json_parsing_formula is None:
            
            parse_rules = [ ( ClientParsing.JSON_PARSE_RULE_TYPE_ALL_ITEMS, None ) ]
            
            json_parsing_formula = ClientParsing.ParseFormulaJSON( parse_rules = parse_rules, content_to_fetch = ClientParsing.JSON_CONTENT_STRING )
            
        
        self._json_parsing_formula = json_parsing_formula
        
    
    def _GetSerialisableInfo( self ):
        
        serialisable_string_processor = self._string_processor.GetSerialisableTuple()
        serialisable_filename_string_converter = self._filename_string_converter.GetSerialisableTuple()
        serialisable_json_parsing_formula = self._json_parsing_formula.GetSerialisableTuple()
        
        return ( serialisable_string_processor, self._remove_actual_filename_ext, self._suffix, serialisable_filename_string_converter, serialisable_json_parsing_formula )
        
    
    def _InitialiseFromSerialisableInfo( self, serialisable_info ):
    
        ( serialisable_string_processor, self._remove_actual_filename_ext, self._suffix, serialisable_filename_string_converter, serialisable_json_parsing_formula ) = serialisable_info
        
        self._string_processor = HydrusSerialisable.CreateFromSerialisableTuple( serialisable_string_processor )
        self._filename_string_converter = HydrusSerialisable.CreateFromSerialisableTuple( serialisable_filename_string_converter )
        self._json_parsing_formula = HydrusSerialisable.CreateFromSerialisableTuple( serialisable_json_parsing_formula )
        
    
    def _UpdateSerialisableInfo( self, version, old_serialisable_info ):
        
        if version == 1:
            
            ( suffix, serialisable_json_parsing_formula ) = old_serialisable_info
            
            string_processor = ClientStrings.StringProcessor()
            
            serialisable_string_processor = string_processor.GetSerialisableTuple()
            
            new_serialisable_info = ( serialisable_string_processor, suffix, serialisable_json_parsing_formula )
            
            return ( 2, new_serialisable_info )
            
        
        if version == 2:
            
            ( serialisable_string_processor, suffix, serialisable_json_parsing_formula ) = old_serialisable_info
            
            remove_actual_filename_ext = False
            filename_string_converter = ClientStrings.StringConverter( example_string = 'my_image.jpg.json' )
            
            serialisable_filename_string_converter = filename_string_converter.GetSerialisableTuple()
            
            new_serialisable_info = ( serialisable_string_processor, remove_actual_filename_ext, suffix, serialisable_filename_string_converter, serialisable_json_parsing_formula )
            
            return ( 3, new_serialisable_info )
            
        
    
    def GetExpectedSidecarPath( self, actual_file_path: str ):
        
        return ClientMetadataMigrationCore.GetSidecarPath( actual_file_path, self._remove_actual_filename_ext, self._suffix, self._filename_string_converter, 'json' )
        
    
    def GetJSONParsingFormula( self ) -> ClientParsing.ParseFormulaJSON:
        
        return self._json_parsing_formula
        
    
    def Import( self, actual_file_path: str ) -> typing.Collection[ str ]:
        
        path = self.GetExpectedSidecarPath( actual_file_path )
        
        if not os.path.exists( path ):
            
            return []
            
        
        try:
            
            with open( path, 'r', encoding = 'utf-8' ) as f:
                
                read_raw_json = f.read()
                
            
        except Exception as e:
            
            raise Exception( 'Could not import from {}: {}'.format( path, str( e ) ) )
            
        
        parsing_context = {}
        collapse_newlines = False
        
        rows = self._json_parsing_formula.Parse( parsing_context, read_raw_json, collapse_newlines )
        
        if self._string_processor.MakesChanges():
            
            rows = self._string_processor.ProcessStrings( rows )
            
        
        return rows
        
    
    def SetJSONParsingFormula( self, json_parsing_formula: ClientParsing.ParseFormulaJSON ):
        
        self._json_parsing_formula = json_parsing_formula
        
    
    def ToString( self ) -> str:
        
        if self._string_processor.MakesChanges():
            
            full_munge_text = ', applying {}'.format( self._string_processor.ToString() )
            
        else:
            
            full_munge_text = ''
            
        
        return 'from JSON sidecar{}'.format( full_munge_text )
        
    

HydrusSerialisable.SERIALISABLE_TYPES_TO_OBJECT_TYPES[ HydrusSerialisable.SERIALISABLE_TYPE_METADATA_SINGLE_FILE_IMPORTER_JSON ] = SingleFileMetadataImporterJSON

class SingleFileMetadataImporterTXT( HydrusSerialisable.SerialisableBase, SingleFileMetadataImporterSidecar ):
    
    SERIALISABLE_TYPE = HydrusSerialisable.SERIALISABLE_TYPE_METADATA_SINGLE_FILE_IMPORTER_TXT
    SERIALISABLE_NAME = 'Metadata Single File Importer TXT'
    SERIALISABLE_VERSION = 3
    
    def __init__( self, string_processor = None, remove_actual_filename_ext = None, suffix = None, filename_string_converter = None ):
        
        if remove_actual_filename_ext is None:
            
            remove_actual_filename_ext = False
            
        
        if suffix is None:
            
            suffix = ''
            
        
        if filename_string_converter is None:
            
            filename_string_converter = ClientStrings.StringConverter( example_string = 'my_image.jpg.txt' )
            
        
        if string_processor is None:
            
            string_processor = ClientStrings.StringProcessor()
            
        
        HydrusSerialisable.SerialisableBase.__init__( self )
        SingleFileMetadataImporterSidecar.__init__( self, string_processor, remove_actual_filename_ext, suffix, filename_string_converter )
        
    
    def _GetSerialisableInfo( self ):
        
        serialisable_string_processor = self._string_processor.GetSerialisableTuple()
        serialisable_filename_string_converter = self._filename_string_converter.GetSerialisableTuple()
        
        return ( serialisable_string_processor, self._remove_actual_filename_ext, self._suffix, serialisable_filename_string_converter )
        
    
    def _InitialiseFromSerialisableInfo( self, serialisable_info ):
    
        ( serialisable_string_processor, self._remove_actual_filename_ext, self._suffix, serialisable_filename_string_converter ) = serialisable_info
        
        self._string_processor = HydrusSerialisable.CreateFromSerialisableTuple( serialisable_string_processor )
        self._filename_string_converter = HydrusSerialisable.CreateFromSerialisableTuple( serialisable_filename_string_converter )
        
    
    def _UpdateSerialisableInfo( self, version, old_serialisable_info ):
        
        if version == 1:
            
            suffix = old_serialisable_info
            
            string_processor = ClientStrings.StringProcessor()
            
            serialisable_string_processor = string_processor.GetSerialisableTuple()
            
            new_serialisable_info = ( serialisable_string_processor, suffix )
            
            return ( 2, new_serialisable_info )
            
        
        if version == 2:
            
            ( serialisable_string_processor, suffix ) = old_serialisable_info
            
            remove_actual_filename_ext = False
            filename_string_converter = ClientStrings.StringConverter( example_string = 'my_image.jpg.txt' )
            
            serialisable_filename_string_converter = filename_string_converter.GetSerialisableTuple()
            
            new_serialisable_info = ( serialisable_string_processor, remove_actual_filename_ext, suffix, serialisable_filename_string_converter )
            
            return ( 3, new_serialisable_info )
            
        
    
    def GetExpectedSidecarPath( self, actual_file_path: str ):
        
        return ClientMetadataMigrationCore.GetSidecarPath( actual_file_path, self._remove_actual_filename_ext, self._suffix, self._filename_string_converter, 'txt' )
        
    
    def Import( self, actual_file_path: str ) -> typing.Collection[ str ]:
        
        path = self.GetExpectedSidecarPath( actual_file_path )
        
        if not os.path.exists( path ):
            
            return []
            
        
        try:
            
            with open( path, 'r', encoding = 'utf-8' ) as f:
                
                raw_text = f.read()
                
            
        except Exception as e:
            
            raise Exception( 'Could not import from {}: {}'.format( path, str( e ) ) )
            
        
        rows = HydrusText.DeserialiseNewlinedTexts( raw_text )
        
        if self._string_processor.MakesChanges():
            
            rows = self._string_processor.ProcessStrings( rows )
            
        
        return rows
        
    
    def ToString( self ) -> str:
        
        if self._string_processor.MakesChanges():
            
            full_munge_text = ', applying {}'.format( self._string_processor.ToString() )
            
        else:
            
            full_munge_text = ''
            
        
        return 'from .txt sidecar'.format( full_munge_text )
        
    

HydrusSerialisable.SERIALISABLE_TYPES_TO_OBJECT_TYPES[ HydrusSerialisable.SERIALISABLE_TYPE_METADATA_SINGLE_FILE_IMPORTER_TXT ] = SingleFileMetadataImporterTXT
