import dxfgrabber
from scipy import interpolate
import numpy as np

class CadReader():
	def __init__(self, file, layer, startKm=0.0, startLevel=0.0, xScale=1, yScale=10):
		self.file=file
		self.layer=layer
		self.startKm=startKm
		self.startLevel=startLevel
		self.xScale=xScale
		self.yScale=yScale

		
		self.read()
		
		
	def read(self):
		self.dxf = dxfgrabber.readfile(self.file)
		self.objects=[entity for entity in self.dxf.entities if entity.layer==self.layer] #and entity.dxftype=='LINE' or entity.dxftype=='LINE' ]
		self.objects=[entity for entity in self.objects if entity.dxftype=='LINE' or entity.dxftype=='POLYLINE' ]
		#x=np.array[entity.points]
		
		self.x=np.array([])
		self.y=np.array([])
		self.przerwyX=[]
		
		for i, entity in enumerate(self.objects):
			if entity.dxftype=="POLYLINE":
				x=np.array([entity.points[i][0] for i in range(len(entity.points))])
				y=np.array([entity.points[i][1] for i in range(len(entity.points))])
				
			elif entity.dxftype=="LINE":
				#assert entity.start[0]<entity.end[0], "Jakas linia ma odwrocona kolejnosc start-end"

				x=np.array([entity.start[0], entity.end[0]])
				y=np.array([entity.start[1], entity.end[1]])
			
			if i==0:
				pass
			else:
				if abs(x.min()-self.x.max())<10:
					pass #Jest zachowana ciaglosc
				else:
					self.przerwyX.append([self.x.max(), x.min()])
			
			self.x=np.append(self.x, x)
			self.y=np.append(self.y, y)
		
		
		
			
		self.xy=np.column_stack((self.x, self.y))
		self.xy=sorted(self.xy, key=lambda k: [k[0], k[1]])
			
		self.xymin=self.xy[0]
			
		self.x=self.x-self.xymin[0]+self.startKm
		self.x=self.x/self.xScale
			
		self.y=self.y-self.xymin[1]
		self.y=self.y/self.yScale+self.startLevel
			
		self.przerwyX=(np.array(self.przerwyX)-self.xymin[0]+self.startKm)/self.xScale

		

				
		self.interline=interpolate.interp1d(self.x, self.y, kind="linear")
	"""
	def getY(self, other, x):
		if x in self.excluded
		for i in self.excluded:
			if x > exc
	"""	
		
if __name__=="__main__":
	niweleta=CadReader(file='profil_pure.dxf', layer='NIWELETA', startKm=3000, startLevel=249.777 ,xScale=1, yScale=10)
	teren=CadReader(file='profil_pure.dxf', layer='TEREN', startKm=niweleta.startKm, startLevel=niweleta.startLevel, xScale=1, yScale=10)
	lewy=CadReader(file='profil_pure.dxf', layer='ROW_L', startKm=niweleta.startKm, startLevel=248.72, xScale=1, yScale=10)
	prawy=CadReader(file='profil_pure.dxf', layer='ROW_P', startKm=niweleta.startKm, startLevel=248.72, xScale=1, yScale=10)
	
	x=3500
	
	print(niweleta.interline(x))
	print(teren.interline(x))
	print(lewy.interline(x))
	print(prawy.interline(x))
	print(lewy.przerwyX)
	
	
	#print(niweleta.interline(x)-teren.interline(x))
	
	#print(niweleta.objects)
	#print(niweleta.objects[1].__dir__())
	#print(niweleta.objects[0].start)