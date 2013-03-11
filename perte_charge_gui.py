#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from perte_charge import *
## import all of the wxPython GUI package
from wxPython.wx import *
## Create a new frame class, derived from the wxPython Frame
import sys


ID_DIAMCTRL=101
ID_DEBITCTRL=102
ID_MATERIAUCTRL=103
ID_PDCCTRL=104
ID_TEMPCTRL=105

class MyFrame(wxFrame):

      def __init__(self, parent, id, title):
          #First, call the base class' __init__ method to create the frame
          wxFrame.__init__(self, parent, id, title,
              wxPoint(100, 100), wxSize(300, 160))

          # Associate some events with methods of this class
          EVT_SIZE(self, self.OnSize)
          EVT_MOVE(self, self.OnMove)

          # Add a panel and some controls to display the size and position
          panel = wxPanel(self, -1)
          wxStaticText(panel, -1, "Diamètre", wxDLG_PNT(panel, wxPoint(4, 5)),wxDefaultSize)
          wxStaticText(panel, -1, "Débit", wxDLG_PNT(panel, wxPoint(4, 20)), wxDefaultSize)
          wxStaticText(panel, -1, "Materiau", wxDLG_PNT(panel, wxPoint(4, 35)),wxDefaultSize)
          wxStaticText(panel, -1, "Perte de charge", wxDLG_PNT(panel, wxPoint(4, 50)), wxDefaultSize)
          wxStaticText(panel, -1, "Température", wxDLG_PNT(panel, wxPoint(4, 65)), wxDefaultSize)

          self.ins_diam=wxStaticText(panel, -1, "(Di : )", wxDLG_PNT(panel, wxPoint(140, 5)), wxDefaultSize)
          self.rugosite=wxStaticText(panel, -1, "(R : mm)", wxDLG_PNT(panel, wxPoint(140, 35)), wxDefaultSize)

          self.diamCtrl = wxTextCtrl(panel,ID_DIAMCTRL, "",wxDLG_PNT(panel, wxPoint(70, 5)),wxDLG_SZE(panel, wxSize(36, -1)),wxTE_PROCESS_ENTER )
          self.debitCtrl = wxTextCtrl(panel,ID_DEBITCTRL, "",wxDLG_PNT(panel, wxPoint(70, 20)),wxDLG_SZE(panel, wxSize(36, -1)),wxTE_PROCESS_ENTER)
          materialChoice=["Acier", "PVC Pr. PN16", "Cuivre", "PEHD PN12,5"]
          self.materiauCtrl = wxChoice(panel,ID_MATERIAUCTRL, wxDLG_PNT(panel,wxPoint(70, 35)),wxDLG_SZE(panel, wxSize(60, -1)), materialChoice)
          self.materiauCtrl.SetSelection(0)
          self.pdcCtrl = wxTextCtrl(panel,ID_PDCCTRL, "",wxDLG_PNT(panel, wxPoint(70, 50)),wxDLG_SZE(panel, wxSize(36, -1)),wxTE_PROCESS_ENTER)
          self.tempCtrl = wxTextCtrl(panel,ID_TEMPCTRL, "20",wxDLG_PNT(panel, wxPoint(70, 65)),wxDLG_SZE(panel, wxSize(36, -1)),wxTE_PROCESS_ENTER)

          wxStaticText(panel, -1, "mm", wxDLG_PNT(panel, wxPoint(110, 5)),wxDefaultSize)
          wxStaticText(panel, -1, "m3/h", wxDLG_PNT(panel, wxPoint(110, 20)), wxDefaultSize)
          wxStaticText(panel, -1, "mm/m", wxDLG_PNT(panel, wxPoint(110, 50)), wxDefaultSize)
          wxStaticText(panel, -1, "°C", wxDLG_PNT(panel, wxPoint(110, 65)), wxDefaultSize)

          EVT_TEXT_ENTER(self,ID_DIAMCTRL, self.OnDiamChange)
          EVT_TEXT_ENTER(self,ID_DEBITCTRL, self.OnDebitChange)
          EVT_TEXT_ENTER(self,ID_PDCCTRL, self.OnPDCChange)
          EVT_TEXT_ENTER(self,ID_TEMPCTRL, self.OnTempChange)
          EVT_CHOICE(self,ID_MATERIAUCTRL, self.OnMaterialChange)


      def whichModified(self):
          if self.diamCtrl.IsModified(): print "diam modifié"
          if self.debitCtrl.IsModified(): print "debit modifié"
          if self.pdcCtrl.IsModified(): print "pdc modifié"
          #if self.materiauCtrl.IsModified(): print "materiau modifié"
          if self.tempCtrl.IsModified(): print "temp modifié"

      def OnDiamChange(self, event):
          self.whichModified()
          print "OnDiamChange called %f" %(float(self.diamCtrl.GetValue()))
          try:
              self.updatePDC()
          except ValueError:
              pass

      def OnDebitChange(self, event):
          self.whichModified()
          self.updatePDC()

      def OnPDCChange(self, event):
          self.whichModified()
          self.updateDiam()

      def OnTempChange(self, event):
          self.whichModified()

      def OnMaterialChange(self, event):
          print event.GetEventType()
          print self.materiauCtrl.GetSelection()
          try:
              self.updatePDC()
          except ValueError:
              pass

      def updatePDC(self):
          result_set=search_headloss_darcy(float(self.debitCtrl.GetValue()),
                                           float(self.diamCtrl.GetValue()),
                                           float(self.materiauCtrl.GetSelection()),
                                           float(self.tempCtrl.GetValue()))
          if result_set:
             self.pdcCtrl.SetValue("%.2f" %(result_set[0]))
             self.diamCtrl.SetValue("%i" %(result_set[1]))
             label="(Di : %3.1f mm)" %(result_set[2])
             self.ins_diam.SetLabel(label)

      def updateDiam(self):
          result=search_diam_darcy(float(self.debitCtrl.GetValue()),
                                           1.15*float(self.pdcCtrl.GetValue()),
                                           float(self.materiauCtrl.GetSelection()),
                                           float(self.tempCtrl.GetValue()))
          if result:
             self.diamCtrl.SetValue("%i" %(result[1]))
             self.pdcCtrl.SetValue("%i" %(result[2]))


      def OnCloseWindow(self, event):
          self.Destroy()

      def OnSize(self, event):
          #size = event.GetSize()
          #self.diamCtrl.SetValue("%s, %s" % (size.width, size.height))
          # tell the event system to continue looking for an event handler,
          # so the default handler will get called.
          event.Skip()

      def OnMove(self, event):
          #pos = event.GetPosition()
          #self.debitCtrl.SetValue("%s, %s" % (pos.x, pos.y))
          pass

# Every wxWindows application must have a class derived from wxApp
class MyApp(wxApp):

      # wxWindows calls this method to initialize the application
      def OnInit(self):
            # Create an instance of our customized Frame class
            frame = MyFrame(NULL, -1, "Calcul perte de charge")
            frame.Show(true)

            self.SetTopWindow(frame)
            # Return a success flag
            return true


app = MyApp(0)     # Create an instance of the application class
app.MainLoop()     # Tell it to start processing events

