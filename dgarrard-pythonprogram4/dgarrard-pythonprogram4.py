import sqlite3
import wx
import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('FINNHUB_API_KEY')

D = datetime.datetime.now()  #date and time as of now, set to global variable D
date = D.strftime("%A %B %d, %Y : %H:%M")  #formats date to days of week, month, day, year, and 24hr time

class dlg_window_error(wx.Dialog):
    def __init__ (self):

        wx.Dialog.__init__ (self, None, title = 'error')



class stock_frame(wx.Frame):
    def __init__ (self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title = title, size = (700,500))  #setup main frame of window
        self.SetMaxSize((700,500))

        data_panel = wx.Panel(self, -1)# setup panel inside frame
        # labels
        self.date_label = wx.StaticText(data_panel, label = "Today's Date",style = wx.ALIGN_CENTER, pos=(95,25))
        self.total_label = wx.StaticText(data_panel, label = 'Total',style = wx.ALIGN_CENTER, pos=(430,25))
        # bottom buttons
        self.disp_data = wx.Button(data_panel, label = 'Display Data', size=(100,-1), pos=(95,410))
        self.cancel = wx.Button(data_panel, label = 'Cancel', size=(100,-1), pos=(450,410))

        self.disp_data.Bind(wx.EVT_BUTTON,self.display_stock_data)  #retrieves data
        self.cancel.Bind(wx.EVT_BUTTON,self.on_cancel)  #closes the program

                            # setup of table and columns
        self.list = wx.ListCtrl(data_panel, -1, style = wx.LC_REPORT, pos=(40,80), size=(600,300))
        self.list.InsertColumn(0, 'company', width=100)
        self.list.InsertColumn(1, 'symbol', width=100)
        self.list.InsertColumn(2, 'purchase price', width=100)
        self.list.InsertColumn(3, 'Shares', width=100)
        self.list.InsertColumn(4, 'current price', width=100)
        self.list.InsertColumn(5, 'gain/loss', width=99)

        self.Centre()
        
    def display_stock_data(self,event):
        try:
            self.date_label.SetLabel(date) #use global date variable to insert into label spot

        
            self.list.DeleteAllItems()  #used to empty the list control
            con = sqlite3.connect('tech_stocks.db')  #connect or create database and assign con variable
            cur = con.cursor()   #assign database to curser for execution of SQL's
            total_gain_loss = 0

            finn = 'https://finnhub.io/api/v1/quote?symbol='

            cur.execute("SELECT company, symbol, purchase_price, shares FROM dow_stocks")  #execute SQL
            counter = 0        
            data = cur.fetchall()  #assign SQL information to data list
            for d in data:  #unpack each line of data to d tuple
            
            
                url = F"{finn}{d[1]}&token={api_key}"  # setup URL to ask for information using finn symbol & api key

                d = [*d]   # change tuple to a list
                #print(url)
                req = requests.get(url)  #data request set to req
                if req.status_code == 200:
                    data_2 = req.json()  #convert data to python dictionary
                    c = data_2['c']   # grab current price from dictionary and assign c
            
                    stock_gain_loss = (c - d[2]) * d[3]   # calculate change in individual stock prices

                    c = f'{c:.2f}'   #convert variable c into float string with 2 decimal places
                    c = [c]     # convert c to a list
                    d = d + c     # add d and c variables together and reassign d
            
                    float(stock_gain_loss) # convert both variables to floats for computations  
                    float(total_gain_loss)
            
                    total_gain_loss = total_gain_loss + stock_gain_loss  # compute the total stock difference
            
                    stock_gain_loss = f'{stock_gain_loss:,.2f}' # convert single stock difference to a float string with 2 decimal places
                    stock_gain_loss = [stock_gain_loss]   # convert to a list
                    data_for_list = d + stock_gain_loss   #assign list d and single stock difference to data_for_list as one big list
            
                    self.list.Append(data_for_list)    # append or cycle through list adding to appropriate column in order     

                else:   #throw error if status code isn't correct (cant reach website)
                    dlg = wx.MessageDialog(None,'cannot connect to website, ensure URL is correct', 'error', wx.OK | wx.ICON_ERROR) 
                    dlg.ShowModal()
                    dlg.Destroy()
                    
        except Exception as err:
            dlg = wx.MessageDialog(self, str(err), 'Error occured') 
            dlg.ShowModal()   # display error message

        total_gain_loss = f'{total_gain_loss:,.2f}'
        total_gain_loss = 'Net gains and losses : $' + total_gain_loss  # convert to float decimal, add strings together
        self.total_label.SetLabel( total_gain_loss )   # send it to change the total difference label  
        self.date_label.SetLabel(date)  # send it to change the date and time on label       
                
    def on_cancel(self,event):
        self.Close()   #close program
                
           
        
        
    
        
           

app = wx.App()    # bring wx python into existence
sf = stock_frame(None, -1, 'Stock Data')   #call parent frame, named stock data and assign to sf
sf.Show()       # show the frame / make visible
app.MainLoop()   # loop looking for events
