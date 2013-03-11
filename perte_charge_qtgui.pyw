# -*- coding: iso-8859-15 -*-

from PyQt4 import QtCore, QtGui, uic
import sys


import perte_charge


base, form = uic.loadUiType("uiPdc.ui")

class Fenetre(QtGui.QWidget):
    
    def __init__(self, parent=None):
        super(Fenetre,self).__init__(parent)
        uic.loadUi("uiPdc.ui",self)
        
        self.CBMateriau.addItems(("Acier", "PVC", "Cuivre", "Multicouche", "PE-X", "PEHD PN12,5", "PEHD PN16"))
        self.change_available_diameter()
        QtCore.QObject.connect(self.CBMateriau, QtCore.SIGNAL("currentIndexChanged(int)"), self.change_available_diameter)
        QtCore.QObject.connect(self.CBDiameter, QtCore.SIGNAL("currentIndexChanged(int)"), self.calculate)
        QtCore.QObject.connect(self.DSBFlowrate, QtCore.SIGNAL("valueChanged(QString)"), self.calculate)
        #QtCore.QObject.connect(self.groupBox, QtCore.SIGNAL("setChecked()"), self.set_info_visibility)
    

    def change_available_diameter(self):
        #print ("selected %i") %self.CBMateriau.currentIndex()
        self.CBDiameter.clear()
        for i in (perte_charge.pipe_size[self.CBMateriau.currentIndex()]):
            #print i
            self.CBDiameter.addItem(str(i[0])) 
        
        
            
    def calculate(self):
        diameter=perte_charge.pipe_size[self.CBMateriau.currentIndex()][self.CBDiameter.currentIndex()][1]
        self.LEResult.clear()
        #print diameter
        #print self.DSBFlowrate.value()
        #print perte_charge.search_headloss_darcy(float(self.DSBFlowrate.value()), diameter, self.CBMateriau.currentIndex())
        result = "%0.2f" %perte_charge.calc_darcy(float(self.DSBFlowrate.value()), diameter, self.CBMateriau.currentIndex())
        #print result
        self.LEResult.setText(result.replace(".",","))
        self.TEInfo.clear()
        self.TEInfo.append("Diamètre intérieur : %0.1f mm" %diameter)
        self.TEInfo.append("Rugosité : %0.3f mm" %perte_charge.roughness_list[self.CBMateriau.currentIndex()])
        self.TEInfo.append("Température : %i °C" %perte_charge.get_water_data_at(20)[0])
        self.TEInfo.append("Masse volumique : %0.1f kg/m3" %perte_charge.get_water_data_at(20)[1])
        self.TEInfo.append("Viscosité : %0.3f " %perte_charge.get_water_data_at(20)[2])
        
 


if (__name__ == "__main__"):
    
    
    app = QtGui.QApplication(sys.argv)
    #app.setStyle("plastique")
    
 
    fenetre=Fenetre()

    fenetre.show()
    
    sys.exit(app.exec_())

    