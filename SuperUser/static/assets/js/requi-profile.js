
    $('#descrip').keyup(function (e) {

            e.preventDefault();
            

              $.ajax({

                type: 'POST',
                url:'/requisitioner/checkPass/',
                data:{
                    
                    'password': $('#descrip').val(),
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),

                },

                    success: function (response) {
                          
                          if (response === "True") {
                               document.getElementById("errorde").innerHTML = ''
                                if ($('#price').val() === '' || $('#quantity').val() === '') {
                                

                                } else {

                                    if ($('#price').val() === $('#quantity').val()) {
                                         
                                         $('#addList').removeAttr('style');
                                    }
                                }
                          }
                          else{
                                 $('#errorde').html('Password do not match');
                                  $('#addList').attr('style','visibility:hidden;');
                                  
                              
                          }
                      }

            });
                
        });


        $('#quantity').keyup(function (e) {
            var pass1 = $('#price').val();
            var pass2 = $('#quantity').val();

            if ($('#descrip').val() === '') {
                
                if (pass1 === pass2) {
                        document.getElementById("errorqu").innerHTML = ''
                    
                    } else {
                        $('#errorqu').html('Password do not match');
                        $('#addList').attr('style','visibility:hidden;');
                    }
            
            } else {
                 if (pass1 === pass2) {
                        document.getElementById("errorqu").innerHTML = ''
                        $('#addList').removeAttr('style');
                    
                    } else {
                        $('#errorqu').html('Password do not match');
                        $('#addList').attr('style','visibility:hidden;');
                    }

            }

           
        });

        $('#price').keyup(function (e) {
            var pass1 = $('#price').val();
            var pass2 = $('#quantity').val();

            if ($('#descrip').val() === '') {
                
                if (pass1 === pass2) {
                        document.getElementById("errorqu").innerHTML = ''
                    
                    } else {
                        $('#errorqu').html('Password do not match');
                        $('#addList').attr('style','visibility:hidden;');
                    }
            
            } else {
                 
                 if (pass1 === pass2) {
                        document.getElementById("errorqu").innerHTML = ''
                        $('#addList').removeAttr('style');
                    
                    } else {
                        $('#errorqu').html('Password do not match');
                        $('#addList').attr('style','visibility:hidden;');
                    }

            }

           
        });


        $('#addList').click(function (e) {
               
            e.preventDefault();
            

              $.ajax({

                type: 'POST',
                url:'/requisitioner/changePass/',
                data:{
                    
                    'password': $('#price').val(),
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),

                },

                    success: function (response) {
                          
                          var newPass = $('#price').val();
                          var display = ''
                          
                          for (var i = newPass.length - 1; i >= 0; i--) {
                              display += '•'
                          }

                          $('#thePassDisplay').html(display);
                          $('#transComp').modal('toggle');
                          toggleModal();
                        

                      }
                      
            });
        })

        function toggleModal(argument) {
            

            $('#descrip').val('');
            $('#price').val('');
            $('#quantity').val('');

            $('#passChange').modal('toggle');

        }