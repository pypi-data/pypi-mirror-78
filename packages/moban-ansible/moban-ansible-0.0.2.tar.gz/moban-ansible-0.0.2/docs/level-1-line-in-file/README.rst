level 1 - lineinfile
======================

It has been requested to have line in file feature from ansible. So far, it supports three parameters.


.. table:: A list of supported commands

   ============ =================== =================================================================
   Parameter    Choices/Defaults    Comments
   ============ =================== =================================================================
   state        'present', 'absent' Whether the line should be there or not.
   regrexp                          The regular expression to look for in every line of the file.
   line                             The line to insert/replace into the file.


Here are currently supported features::

    targets:
      # remove a line from a file
      - output: absent.txt
        template: absent_file.txt
        template_type:
          base_type: lineinfile
          options:
            state: absent
            regexp: "^remove.*$"
      # ensure a line in a file
      - output: ensure.txt
        template: ensure_file.txt
        template_type:
          base_type: lineinfile
          options:
            regexp: "^code="
            line: "code=C"
      # append a line to a file
      - output: append.txt
        template: append_file.txt
        template_type:
          base_type: lineinfile
          options:
            line: "127.0.0.1 append"
