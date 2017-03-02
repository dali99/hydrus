import ClientConstants as CC
import ClientGUICommon
import ClientGUIDialogs
import ClientGUIFrames
import ClientGUIScrolledPanels
import ClientGUIPanels
import ClientThreading
import HydrusConstants as HC
import HydrusData
import HydrusGlobals
import HydrusNATPunch
import os
import traceback
import wx

class ReviewServicesPanel( ClientGUIScrolledPanels.ReviewPanel ):
    
    def __init__( self, parent, controller ):
        
        self._controller = controller
        
        ClientGUIScrolledPanels.ReviewPanel.__init__( self, parent )
        
        self._notebook = wx.Notebook( self )
        
        self._local_listbook = ClientGUICommon.ListBook( self._notebook )
        self._remote_listbook = ClientGUICommon.ListBook( self._notebook )
        
        self._InitialiseServices()
        
        self._notebook.AddPage( self._local_listbook, 'local' )
        self._notebook.AddPage( self._remote_listbook, 'remote' )
        
        self.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.EventPageChanged )
        
        vbox = wx.BoxSizer( wx.VERTICAL )
        
        vbox.AddF( self._notebook, CC.FLAGS_EXPAND_BOTH_WAYS )
        
        self.SetSizer( vbox )
        
        self._controller.sub( self, 'RefreshServices', 'notify_new_services_gui' )
        
    
    def _InitialiseServices( self ):
        
        self._local_listbook.DeleteAllPages()
        self._remote_listbook.DeleteAllPages()
        
        listbook_dict = {}
        
        services = self._controller.GetServicesManager().GetServices( randomised = False )
        
        for service in services:
            
            service_type = service.GetServiceType()
            
            if service_type in HC.LOCAL_SERVICES: parent_listbook = self._local_listbook
            else: parent_listbook = self._remote_listbook
            
            if service_type == HC.TAG_REPOSITORY: name = 'tag repositories'
            elif service_type == HC.FILE_REPOSITORY: name = 'file repositories'
            elif service_type == HC.MESSAGE_DEPOT: name = 'message depots'
            elif service_type == HC.SERVER_ADMIN: name = 'administrative servers'
            elif service_type in HC.LOCAL_FILE_SERVICES: name = 'files'
            elif service_type == HC.LOCAL_TAG: name = 'tags'
            elif service_type == HC.LOCAL_RATING_LIKE: name = 'like/dislike ratings'
            elif service_type == HC.LOCAL_RATING_NUMERICAL: name = 'numerical ratings'
            elif service_type == HC.LOCAL_BOORU: name = 'booru'
            elif service_type == HC.IPFS: name = 'ipfs'
            else: continue
            
            if name not in listbook_dict:
                
                listbook = ClientGUICommon.ListBook( parent_listbook )
                
                listbook_dict[ name ] = listbook
                
                parent_listbook.AddPage( name, name, listbook )
                
            
            listbook = listbook_dict[ name ]
            
            name = service.GetName()
            
            panel_class = ClientGUIPanels.ReviewServicePanel
            
            listbook.AddPageArgs( name, name, panel_class, ( listbook, service ), {} )
            
        
    
    def EventPageChanged( self, event ):
        
        wx.PostEvent( self.GetParent(), CC.SizeChangedEvent( -1 ) )
        
    
    def DoGetBestSize( self ):
        
        # this overrides the py stub in ScrolledPanel, which allows for unusual scroll behaviour driven by whatever this returns
        
        # wx.Notebook isn't expanding on page change and hence increasing min/virtual size and so on to the scrollable panel above, nullifying the neat expand-on-change-page event
        # so, until I write my own or figure out a clever solution, let's just force it
        
        if hasattr( self, '_notebook' ):
            
            current_page = self._notebook.GetCurrentPage()
            
            ( notebook_width, notebook_height ) = self._notebook.GetSize()
            ( page_width, page_height ) = current_page.GetSize()
            
            extra_width = notebook_width - page_width
            extra_height = notebook_height - page_height
            
            ( page_best_width, page_best_height ) = current_page.GetBestSize()
            
            best_size = ( page_best_width + extra_width, page_best_height + extra_height )
            
            return best_size
            
        else:
            
            return ( -1, -1 )
            
        
    
    def RefreshServices( self ):
        
        self._InitialiseServices()
        
    
