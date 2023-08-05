import datetime,builtins,platform,time,math,os,urllib
from urllib import request
IS_WIN=False if platform.system().find('Linux')>-1 else True
NOW=datetime.datetime.now()
NOW_TS=math.floor(NOW.timestamp())
NOW=NOW.strftime('%Y-%m-%d %H:%M:%S')
def is_numeric(x):
	try:float(x);return True
	except:return False
def now(x=None):#
	if x is None:return int(datetime.datetime.now().timestamp())
	elif isinstance(x,int):return datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S')
	else:
		try: import dateutil.parser;return int(dateutil.parser.parse(x).timestamp())
		except Exception: return int(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').timestamp())
def print(*a,func=None,time='%m/%d %H:%M:%S',pretty=False,**s):
	a=list(a)
	if func:
		for i,x in enumerate(a):
			a[i]=func(x)
	if time:
		a.insert(0,datetime.datetime.now().strftime(time)+' :')
	if pretty:
		import pprint
		for x in a:
			pprint.pprint(x)
	else:
		builtins.print(*a,**s)
def diff(a,b):
	diff={}
	for x in a:
		if b.get(x)!=a[x]: diff[x]=[a[x],b.get(x)]
	return diff
def notice(x,c='default'):request.urlopen(r'http://call.ff2.pw/?%s=%s&passwd=frank'%(c,urllib.parse.quote_plus(x)))
def rand_sleep(i=0.4,a=0.8):import random;time.sleep(random.randint(i*1000,a*1000)/1000);
def rand(i=9,a=None):import random;return random.randint(int(i),int(a)) if a else random.randint(0,int(i-1));
def md5(x):import hashlib;hl = hashlib.md5();hl.update(x.encode('utf-8') if isinstance(x,str) else x);return hl.hexdigest();
def bin2hex(x):import binascii;return binascii.hexlify(x.encode('utf-8') if isinstance(x,str) else x);
def base64_encode(x):import base64;return base64.b64encode(x) if isinstance(x,bytes) else base64.b64encode(x.encode('utf-8'))
def base64_decode(x):import base64;return base64.b64decode(x)
def log(*x,path=None):
	if path is None:
		path='/tmp/frank.log' if os.path.exists('/tmp') else './FPC.log'
	with open(path,'a',encoding='utf-8') as f:
		print(*x,file=f)
def parse(o):#print class/obj's attr beatiful
	method=[];attr=[]
	for x in dir(o):
		if x[:2]=='__':continue
		method.append(x) if callable(getattr(o,x)) else attr.append(x)
	builtins.print('method',method)
	builtins.print('attr',attr)
def obj(obj=None,remote=False):#save or open a python varible
	import pickle
	if remote:
		return pickle.loads(request.urlopen(r'http://a.ff2.pw/obj.php').read()) if obj is None else request.urlopen(r'http://a.ff2.pw/obj.php',pickle.dumps(obj))
	else:
		path='/tmp/frank.data' if os.path.exists('/tmp') else './FPC.data'
		return pickle.load(open(path,'rb')) if obj is None else pickle.dump(obj,open(path,'wb'))
class mysql(object):
	def __init__(self, key=127,**args):
		import pymysql
		self.pymysql=pymysql
		_CONNECT_CONFIG={127:{'host':'127.0.0.1','user':'root','password':'','db':'localhost','charset':'utf8','cursorclass':pymysql.cursors.DictCursor}}
		connect_config = _CONNECT_CONFIG[key]
		if 'table' in args:
			self.table=args['table']
			del args['table']
		for x in args:
			connect_config[x]=args[x]
		self.conn = pymysql.connect(**connect_config)
	def __getattr__(self,attr):
		return getattr(self.conn,attr)
	def _split_dict(self,dicts,splitor=','):
		string=''
		for x in dicts:
			if isinstance(dicts[x],(int,float)):
				data=dicts[x]
			elif dicts[x] is None:
				data='NULL'
			else:
				data='"'+self.pymysql.escape_string(dicts[x])+'"'
			string+=r' `%s`=%s %s'%(x,data,splitor)
		return string[:-len(splitor)]
	def _split_add_dict(self,dicts):
		key=value=''
		for x in dicts:
			key+=r'`%s`,'%x
			if dicts[x] is None:value+='null,'
			else:value+=r'%s,'%(dicts[x]) if is_numeric(dicts[x]) else r'"%s",'%(self.pymysql.escape_string(dicts[x]))
		return key[:-1],value[:-1]
	def execute(self,strs):
		strs=strs.strip()
		is_query = True if strs[:4].lower() in ['sele','show'] else False
		with self.conn.cursor() as cur:
			data=cur.execute(strs)
			data=cur.fetchall() if is_query else cur.lastrowid
		is_query or self.conn.commit()
		return data
	def add(self,dicts,table=None):
		'''table is optional,dicts can be list or dict'''
		if not isinstance(table,str):
			if table is None:
				table=self.table
			else:#table is not none and reverse two args
				table_=dicts
				dicts=table
				table=table_
		if isinstance(dicts,dict): dicts=[dicts]
		values=''#values like (1,2),(2,3) 
		for x in dicts:
			key,value=self._split_add_dict(x)
			values+=r'(%s),'%(value)
		return self.execute(r''' insert `%s`(%s) values%s '''%(table,key,values[:-1]))
	def update(self,where,data,table=None):
		'''where can be str or dict'''
		if table is None:
			table=self.table
		if isinstance(where,dict) : where=self._split_dict(where,'and')
		data=self._split_dict(data)
		return self.execute(r''' update `%s` set %s where %s'''%(table,data,where))
class redis(object):
	server=False
	def __init__(self,host='127.0.0.1',db=0,port=6379,ssh_host=None,ssh_username='root',ssh_password=None):
		import redis
		if ssh_host:
			import sshtunnel
			sshtunnel.DAEMON=True 
			sshtunnel.SSHTunnelForwarder.daemon_forward_servers=True
			sshtunnel.SSHTunnelForwarder.daemon_transport=True
			self.server = sshtunnel.SSHTunnelForwarder(ssh_address_or_host=ssh_host,ssh_username=ssh_username,ssh_password=ssh_password,remote_bind_address=(host,6379))
			self.server.start()
			port=self.server.local_bind_port
		self.redis=redis.StrictRedis(host=host, port=port, db=db,decode_responses=True)
	def __getattr__(self,attr):
		return getattr(self.redis,attr)
def process(target,is_thread=True,join=False,num=None,sleep=None,**args):
	if isinstance(target,str):#args:target,[sync]
		import subprocess
		proc=subprocess.Popen(target,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True);
		return proc.communicate() if args.get('sync') else None
	pros=[]
	if 'args' in args:
		if isinstance(args['args'],list):
			args_list=args['args']
			if num is None:num=len(args_list)
		else:args_list=[args['args']]*num
	if num is None:num=1
	if is_thread:
		import threading
		for x in range(num):
			if 'args' in args:
				args['args']=args_list[x] if isinstance(args_list[x],(tuple,list)) else [args_list[x]]
			pros.append(threading.Thread(target=target,**args))
			pros[-1].start()
			if sleep:time.sleep(sleep)
	else:
		from multiprocessing import Process
		for x in range(num):
			if 'args' in args:
				args['args']=args_list[x] if isinstance(args_list[x],(tuple,list)) else [args_list[x]]
			pros.append(Process(target=target,**args))
			pros[-1].start()
			if sleep:time.sleep(sleep)
	if join:
		for x in range(num):
			pros[x].join()
	return pros