tail -f output.txt | grep -E --line-buffered param_ | while read line; do echo ${line}; done

tail -f /logs/output.txt | \
 grep -E --line-buffered reads | \
 while read line; do \
 echo ${line}; done

 tail -f <file> | sed '/string/s/stuff//g' >>