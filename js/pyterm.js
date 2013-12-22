/**
 * Created with SublimeText3
 * User: alessandro
 * Date: 17/07/13
 * Time: 12.41
 */
jQuery(document).ready(function($) {
    var id = 1;
    $('#pyterm').terminal(function(command, term) {
        if (command == 'help') {
            term.echo("available commands are log, search, info");
        } else if (command == 'log'){
            term.push(function(command, term) {
                if (command == 'help') {
                    term.echo('you can digitate list to show all log files or one log file to select it');
                } else if (command == 'list') {
                    term.push({
                      source: "/log_list",
                      messages: {
                          noResults: '',
                          results: function () { term: '*'
                          }
                      }
                  });}
                  else if (command == 'test') {
                    term.push(function () {
                      var postdata = {term: 'cat', log: '2013_07_29', calc: '1'};
                      $.post('/log_sub', postdata, function (data) {
                          // and set the title with the result
                          $("#pyterm").html(data);
                      });
                      return false;
                  });
                } else {
                    term.echo('unknown command ' + command);
                }
            }, {
                prompt: 'log> ',
                name: 'log'});
        } else if (command == "js") {
            term.push(function(command, term) {
                var result = window.eval(command);
                if (result != undefined) {
                    term.echo(String(result));
                }
            }, {
                name: 'js',
                prompt: 'js> '});
        } else if (command == 'mysql') {
            term.push(function(command, term) {
                term.pause();
                $.jrpc("mysql-rpc-demo.php",
                       id++,
                       "query",
                       [command],
                       function(data) {
                           term.resume();
                           if (data.error) {
                               term.error(data.error.message);
                           } else {
                               if (typeof data.result == 'boolean') {
                                   term.echo(data.result ? 'success' : 'fail');
                               } else {
                                   var len = data.result.length;
                                   for(var i=0;i<len; ++i) {
                                       term.echo(data.result[i].join(' | '));
                                   }
                               }
                           }
                       },
                       function(xhr, status, error) {
                           term.error('[AJAX] ' + status +
                                      ' - Server reponse is: \n' +
                                      xhr.responseText);
                           term.resume();
                       });
            }, {
                greetings: "This is example of using mysql from terminal\n\
you are allowed to execute: select, insert, update and delete from/to table:\n\
    table test(integer_value integer, varchar_value varchar(255))",
                prompt: "mysql> "});
        } else {
            term.echo("unknow command " + command);
        }
    }, {
        greetings: "multiply terminals demo use help to see available commands",
        onBlur: function() {
            // prevent loosing focus
            return false;
        }
    });
});