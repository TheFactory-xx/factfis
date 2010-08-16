#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#/****************************************************************************
#*
#* Andres Hocevar 2010-2011
#*
#* consola.py
#* licencia GPL v3
#* Permite gestiona la impresora fiscal como linea de comandos
#*          http://code.google.com/p/factfis
#***************************************************************************/
import cmd
import fiscales

imp = fiscales.factfis();
imp.mdepura=True

class Console(cmd.Cmd):
	prompt = "#> "

	def __init__ (self):
		cmd.Cmd.__init__(self)

	def do_send (self, cmd):
		cmd=cmd.replace('"','',1)
		cmd=cmd.replace("'",'',1)
		imp.SimpleCmd(cmd)

	def do_query (self, cmd):
		if imp.QueryCmd(cmd):
			msj=1
			while msj!=None:
				msj=imp.FecthRow()

	def do_mensaje(self, cmd):
		imp.SimpleCmd('810'+cmd[0:40])

	def do_reset(self, cmd):
		imp.SimpleCmd('e')

	def do_estado1(self, cmd):
		imp.mdepura=False
		print imp.estado1()
		imp.mdepura=True

	def do_getserial(self, cmd):
		imp.mdepura=False
		if imp.QueryCmd('S1'):
			msj=1
			while True:
				msj=imp.FecthRow()
				if msj==None:
					break
				m=msj.split(chr(10))
				if len(m)>=9:
					print m[9]
		imp.mdepura=True

	def do_getrif(self, cmd):
		imp.mdepura=False
		if imp.QueryCmd('S1'):
			msj=1
			while True:
				msj=imp.FecthRow()
				if msj==None:
					break
				m=msj.split(chr(10))
				if len(m)>=8:
					print m[8]
		imp.mdepura=True

	def do_getultimo(self, cmd):
		imp.mdepura=False
		if imp.QueryCmd('S1'):
			msj=1
			while True:
				msj=imp.FecthRow()
				if msj==None:
					break
				m=msj.split(chr(10))
				if len(m)>=2:
					print m[2]
		imp.mdepura=True

	def do_ultimo(self, cmd):
		imp.SimpleCmd('RU00000000000000')

	def do_prog(self, cmd):
		imp.SimpleCmd('D')

	def do_display(self, cmd):
		imp.SimpleCmd('STXcU'+cmd[0:20])

	def do_cierrex(self, cmd):
		imp.SimpleCmd('I0X')

	def do_cierrez(self, cmd):
		imp.SimpleCmd('I0Z')

	def do_anula(self, cmd):
		imp.SimpleCmd('7')

	def do_gaveta(self, cmd):
		imp.SimpleCmd('w')

	def do_version(self, cmd):
		imp.SimpleCmd('x')

	def do_status (self, cmd):
		print imp.ReadFpStatus()
		print 'status: '+imp.status
		print 'error : '+imp.error

	def do_quit (self, s):
		return True

	def help_display(self):
		print "Envia un mensaje al display"

	def help_send (self):
		print "Envia un comando simple a la impresora (devuelve ACK o NAK)"

	def help_prog (self):
		print "Imprime la programacion de la impresora"

	def help_cierrex (self):
		print "Imprime un reporte X"

	def help_anula (self):
		print "Anula la factura pendiente"

	def help_cierrez (self):
		print "Imprime un reporte Z"

	def help_query(self):
		print "Envia un comando de lectura a la impresora"

	def help_version(self):
		print "Imprime la version del firmware"

	def help_mensaje(self):
		print "Imprime un mensaje por la impresora"

	def help_help(self):
		print "Ayuda"

	def help_status(self):
		print "Consulta el estatus de la impresora"

	def help_reset(self):
		print "Envia un reset a la impresora"

	def help_gaveta(self):
		print "Apertura de gaveta"

	def help_gaveta(self):
		print "Imprime el ultimo documento guardado"

	def help_quit (self):
		print "Sale de la  consola"

	#def complete_get_color (self, text, line, begidx, endix):
	#	return [i for i in self._colors if i.startswith(text)]

	#do_EOF   = do_quit
	#help_EOF = help_quit

if __name__ == "__main__":
	if imp.puerto != None:
		console = Console()
		try:
			console.cmdloop("Impresora conectada a:"+imp.puerto)
		except KeyboardInterrupt:
			imp.CloseFpctrl()
			console.do_quit(None)
