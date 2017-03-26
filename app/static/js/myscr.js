
         $('[data-toggle="tooltip"]').tooltip(); 

// Promena na statusot na Oglas
$('.klikPromena').on('click', function() {
               if($(this).find('abbr').text() == 'Слободен'){
                  $(this).removeClass('btn-success').addClass('btn-danger')
                  $(this).find('abbr').text('Зафатен')
                  $(this).find('span').removeClass('glyphicon-star').addClass('glyphicon-star-empty')
               }
               else{
                   $(this).find('abbr').text('Слободен')
                   $(this).removeClass('btn-danger').addClass('btn-success')
                   $(this).find('span').removeClass('glyphicon-star-empty').addClass('glyphicon-star')
               }

            var data = {}
            data['conId'] = ($(this).attr('id'))

            $.ajax({
                type : "POST",
                url : "/condoStatusChange",
                data: JSON.stringify(data, null, '\t'),
                contentType: 'application/json;charset=UTF-8',
                success: function(result) {
                }
            });
        });


        // Promena na preferencite
           var datas = {}
        $('#cbx').on('change', function () {
            if($(this).is(':checked')){
                console.log('checked');
                $('#savePref').show('slow')
            }else{
                datas['tick'] = 0;
                datas['userid'] = $('#userid').val();
                $.ajax({
                type : "POST",
                url : "/savePreferences",
                data: JSON.stringify(datas, null, '\t'),
                contentType: 'application/json;charset=UTF-8',
                success: function(result) {
                    $('#personalPref').hide('slow')
                    $('#savePref').show('slow')
                }
            });
            }
        })


            // Zacuvuvanje na preferenci
        $('#savePref').on('click', function () {
            $('#lbl').text('Активирано (Клик за Деактивација)')
            $('#spn').text('Опцијата ви е активирана. Доколку не сакате да добивате е-маил известување - кликнете на „Деактивирај“.')
            datas['userid'] = $('#userid').val()
            datas['tick'] = 1;
            datas['od'] = $('#od').val();
            datas['doo'] = $('#doo').children('input').val()
            datas['types'] = $('#condoType').val();
            datas['city'] = $('#city').val();
            datas['area'] = $('#areas').val();
            $('#savePref').hide('slow')

            $.ajax({
                type : "POST",
                url : "/savePreferences",
                data: JSON.stringify(datas, null, '\t'),
                contentType: 'application/json;charset=UTF-8',
                success: function(result) {
                }
            });

        });



        if($('#cbx').is(":checked")){
            $('#lbl').text('Активирано (Клик за Деактивација)')
            $('#spn').text('Опцијата ви е активирана. Доколку не сакате да добивате е-маил известување - кликнете на „Деактивирај“.')
            $('#personalPref').show()
            $('#savePref').hide()
        }

        $("#cbx").change(function() {
            if(this.checked) {
                $('#personalPref').show('slow')
            }else{
                $('#personalPref').hide('slow')
                $('#lbl').text('Активирај')
                $('#spn').text('Доколку ја активирате оваа опција - ќе добиете е-маил известување доколку некој нов оглас ги исполнува вашите критериуми.')
            }
        });

             $('#city').on('change', function() {
              if(this.value != 'Скопје'){
                  $('#areas').parent().parent().hide('slow')
                  $('#areas').val('Центар')
              }else{
                  $('#areas').parent().parent().show('slow')
                  $('#areas').show('slow')
                  $('#areas').val('Центар')
              }
            });


        $('#condoType').on('change', function() {
        if ( $('#condoType').val() == 0){
           $('#od').prop('placeholder', 'Пр: 50000')
           $('#doo').prop('placeholder', 'Пр: 80000')
        }else{
         $('#od').prop('placeholder', 'Пр: 150')
           $('#doo').prop('placeholder', 'Пр: 200')
        }
        });

        condoType = $('#condoType').attr('value'); $('#condoType option[value='+condoType+']').prop('selected', true);
        city = $('#city').attr('value'); $('#city option[value='+city+']').prop('selected', true);
        if($('#city').attr('value') != 'Скопје'){
            $('#areas').parent().parent().hide();
        }else{
        areas = $('#areas').attr('value'); $('#areas option[value='+areas+']').prop('selected', true);
        }
        $('#doo').children('input').val($('#dooVal').val());



