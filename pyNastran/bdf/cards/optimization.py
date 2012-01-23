from baseCard import BaseCard

class OptConstraint(BaseCard):
    def __init__(self):
        pass

class DCONSTR(OptConstraint):
    type = 'DCONSTR'
    def __init__(self,card=None,data=None):
        if card:
            self.oid    = card.field(1)
            self.rid    = card.field(2)
            self.lid    = card.field(3,-1e20)
            self.uid    = card.field(4, 1e20)
            self.lowfq  = card.field(5,0.0)
            self.highfq = card.field(6,1e20)
        else:
            self.oid    = data[0]
            self.rid    = data[1]
            self.lid    = data[2]
            self.uid    = data[3]
            self.lowfq  = data[4]
            self.highfq = data[5]
        ###

    def rawFields(self):
        fields = ['DCONSTR',self.oid,self.rid,self.lid,self.uid,self.lowfq,self.highfq]
        return fields

    def reprFields(self):
        lid    = self.setBlankIfDefault(self.lid,-1e20)
        uid    = self.setBlankIfDefault(self.uid, 1e20)
        lowfq  = self.setBlankIfDefault(self.lowfq,0.0)
        highfq = self.setBlankIfDefault(self.highfq,1e20)
        fields = ['DCONSTR',self.oid,self.rid,lid,uid,lowfq,highfq]
        return fields

class DESVAR(OptConstraint):
    type = 'DESVAR'
    def __init__(self,card=None,data=None):
        self.oid = card.field(1)
        self.label = card.field(2)
        self.xinit = card.field(3)
        self.xlb   = card.field(4,-1e20)
        self.xub   = card.field(5, 1e20)
        self.delx  = card.field(6, 1e20)
        self.ddval = card.field(7)
    
    def rawFields(self):
        fields = ['DESVAR',self.oid,self.label,self.xinit,self.xlb,self.xub,
        self.delx,self.ddval]
        return fields

    def reprFields(self):
        xlb  = self.setBlankIfDefault(self.xlb, -1e20)
        xub  = self.setBlankIfDefault(self.xub,  1e20)
        delx = self.setBlankIfDefault(self.delx, 1e20)
        fields = ['DESVAR',self.oid,self.label,self.xinit,xlb,xub,
        delx,self.ddval]
        return fields

class DDVAL(OptConstraint):
    type = 'DDVal'
    def __init__(self,card=None,data=None):
        self.oid = card.field(1)
        self.dval1 = card.field(2)
        self.dval2 = card.field(3)
        self.dval3 = card.field(4)
        self.dval4 = card.field(5)
        self.dval5 = card.field(6)
        self.dval6 = card.field(7)
        self.dval7 = card.field(8)
    
    def rawFields(self):
        fields = ['DDVAL',self.oid,self.dval1,self.dval2,self.dval3,
                  self.dval4,self.dval5,self.dval6,self.dval7]
        return self.printCard(fields)

class DRESP1(OptConstraint):
    type = 'DRESP1'
    def __init__(self,card=None,data=None):
        """
        DRESP1         1S1      CSTRAIN PCOMP                  1       1   10000
        """
        self.oid    = card.field(1)
        self.label  = card.field(2)
        self.rtype  = card.field(3)
        self.ptype  = card.field(4)
        self.region = card.field(5)
        self.atta   = card.field(6)
        self.attb   = card.field(7)
        self.atti   = card.field(8)
        self.others = card.fields(9)
        #if self.others:
        #    print "self.others = ",self.others
        #    print str(self)
        #assert len(self.others)==0
    
    def rawFields(self):
        fields = ['DRESP1',self.oid,self.label,self.rtype,self.ptype,self.region,self.atta,self.attb,self.atti
                           ]+self.others
        return fields

class DVPREL1(OptConstraint):
    type = 'DVPREL1'
    def __init__(self,card=None,data=None):
        """
        DVPREL1   200000   PCOMP    2000      T2
                  200000     1.0
        """
        self.oid    = card.field(1)
        self.Type   = card.field(2)
        self.pid    = card.field(3)
        self.pNameFid = card.field(4)
        self.pMin   = card.field(5)
        self.pMax   = card.field(6,1e20)
        self.c0     = card.field(7,0.0)
            
        self.dvids  = []
        self.coeffs = []
        endFields = card.fields(9)
        #print "endFields = ",endFields
        nFields = len(endFields)-1
        if nFields%2==1:
            endFields.append(None)
            nFields+=1
        i = 0
        for i in range(0,nFields,2):
            self.dvids.append(endFields[i])
            self.coeffs.append(endFields[i+1])
        if nFields%2==1:
            print card
            print "dvids = ",self.dvids
            print "coeffs = ",self.coeffs
            print str(self)
            raise Exception('invalid DVPREL1...')

    def crossReference(self,model):
        self.pid = model.Property(self.pid)
    
    def Pid(self):
        if isinstance(self.pid,int):
            return self.pid
        return self.pid.pid

    def rawFields(self):
        fields = ['DVPREL1',self.oid,self.Type,self.Pid(),self.pNameFid,self.pMin,self.pMax,self.c0,None]
        for dvid,coeff in zip(self.dvids,self.coeffs):
            fields.append(dvid)
            fields.append(coeff)
        return fields

    def reprFields(self):
        pMax = self.setBlankIfDefault(self.pMax,1e20)
        c0   = self.setBlankIfDefault(self.c0,0.)
        fields = ['DVPREL1',self.oid,self.Type,self.Pid(),self.pNameFid,self.pMin,pMax,c0,None]
        for dvid,coeff in zip(self.dvids,self.coeffs):
            fields.append(dvid)
            fields.append(coeff)
        return fields
