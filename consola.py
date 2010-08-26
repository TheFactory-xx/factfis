#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
 #* OEOG Envia un archivo a la impresora fiscal
 #*
 #*
 #* @version   Beta 1
 #* @author    Andres Hocevar
 #*
 #* @since     Agosto 10 del 2010
 #**/
 #/***************************************************************************
 #*
 #* Este programa es software libre: usted puede redistribuirlo y / o modificar
 #* bajo los términos de la GNU General Public License publicada por
 #* la Free Software Foundation, bien de la versión 3 de la Licencia, o
 #* (A su elección) cualquier versión posterior.
 #*
 #* Este programa se distribuye con la esperanza de que sea útil,
 #* pero SIN NINGUNA GARANTÍA, incluso sin la garantía implícita de
 #* COMERCIALIZACIÓN o IDONEIDAD PARA UN PROPÓSITO PARTICULAR. Ver la
 #* Licencia Pública General GNU para más detalles.
 #*
 #* Debería haber recibido una copia de la GNU General Public License
 #* junto con este programa. Si no, véase <http://www.gnu.org/licenses/>.
 #*
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
		text=self.wrap(cmd,40)
		for msj in text.split('\n'):
			imp.SimpleCmd('800'+msj[0:39])
		imp.SimpleCmd('810')

	def do_encabc(self,cmd):
		arr=cmd.split(' ',1)
		ln=arr[0].zfill(2)
		msj='PH'+ln+arr[1][0:39].center(40)
		imp.SimpleCmd(msj)

	def do_reset(self, cmd):
		imp.SimpleCmd('e')

	def do_bandera(self, cmd):
		arr=cmd.split(' ',1)
		ln=arr[0].zfill(2)
		lo=arr[1].zfill(2)
		msj='PJ'+ln+lo
		imp.SimpleCmd(msj)

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

	def do_leer(self, cmd):
		imp._read(1)

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

	def help_leer(self):
		print "Lee 1 byte"

	def help_encabc(self):
		print "Envia el encabezado para los documentos "
		print "Ej. encabc [1-8] TITULO DE EJEMPLO"

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

	def help_bandera(self):
		print "Asigna valores a las banderas"
		print "Ej. bandera 0 0"

	def help_gaveta(self):
		print "Imprime el ultimo documento guardado"

	def help_quit (self):
		print "Sale de la  consola"

	#def complete_get_color (self, text, line, begidx, endix):
	#	return [i for i in self._colors if i.startswith(text)]

	do_e   = do_reset
	do_QUIT = do_quit
	do_exit = do_quit
	do_EXIT = do_quit

	def wrap(self,text, width):
		return reduce(lambda line, word, width=width: '%s%s%s' % (line,' \n'[(len(line)-line.rfind('\n')-1+ len(word.split('\n',1)[0]) >= width)],word),text.split(' '))

if __name__ == "__main__":
	if imp.puerto != None:
		console = Console()
		try:
			console.cmdloop("Impresora conectada a:"+imp.puerto)
		except KeyboardInterrupt:
			imp.CloseFpctrl()
			console.do_quit(None)
