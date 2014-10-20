######################################
#  liquidsoap broadcast monitoring   #
######################################

# author Jonas Ohrstrom <jonas@digris.ch>


########################################
# include configuration                #
########################################

%include "ls_config.liq"

# log
set("log.file.path",log_file)
set("log.stdout", true)
set("log.level",log_level)

# telnet server
set("server.telnet", true)


########################################
# monitoring setup                     #
########################################

silence = single("/storage/pypo/files/basic/silence.mp3")

# default
default = silence



def notify(m)
  print('notify')
  print(m['title'])
  print(m['artist'])
  print(m['channel'])
  
  title = quote(m['title'])
  
  command = "./notify.sh --metadata --channel=#{m['channel']} --title=#{title}"
  print(command)
  system(command)
  
end




#########################################
# include stations, edit/add in file
#########################################

%include "include_stations.liq"









    


