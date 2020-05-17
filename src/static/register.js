const button = document.querySelector('.btn')
const form   = document.querySelector('.form')
/*
button.addEventListener('click', function() {
   form.classList.add('form--no') 
});
*/
check_name = function(value){
   let csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
   data = {check_username: value};
   $.ajax({
       url: '/profiles/register/',
       type: 'POST',
       data: data,
       success: function(data){
           if (!data['name_available']) {
           $('input[name ="username"]')[0].style.boxShadow = "0 0 2px 1px rgba(245, 0, 0, 0.7), 0 2px 2px 0 rgba(245, 0, 0, 0.7)";
           document.getElementById('error-message').text = "Username is already taken!"; }
           if(data['name_available']) {
           $('input[name ="username"]')[0].style.boxShadow = "0 0 2px 1px rgba(0, 180, 0, 0.7), 0 2px 2px 0 rgba(0, 180, 0, 0.7)";
           document.getElementById('error-message').text = "";}
           },
       beforeSend: function (xhr) {
           xhr.setRequestHeader("X-CSRFToken", `${csrf_token}`);
       },
       dataType: 'json',
   });
}

check_email = function(value){
   let csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
   data = {check_mail: value};
   $.ajax({
       url: '/profiles/register/',
       type: 'POST',
       data: data,
       success: function(data){
           if (!data['mail_available']) {
           $('input[name ="email"]')[0].style.boxShadow = "0 0 2px 1px rgba(245, 0, 0, 0.7), " +
                                                          "0 2px 2px 0 rgba(245, 0, 0, 0.7)";
           document.getElementById('error-message').text = "Email is already taken!"; }
           if(data['mail_available']) {
           $('input[name ="email"]')[0].style.boxShadow = "0 0 2px 1px rgba(0, 180, 0, 0.7), " +
                                                          "0 2px 2px 0 rgba(0, 180, 0, 0.7)";
           document.getElementById('error-message').text = "";}
           },
       beforeSend: function (xhr) {
           xhr.setRequestHeader("X-CSRFToken", `${csrf_token}`);
       },
       dataType: 'json',
   });
}

show_comments = function(elem){
   let comments = $(elem).parents()[2].children[3];
   let display =  $(comments).css("display");
   if(display === "none") {
       $(comments).show();
   } else {
       $(comments).hide();
   }
}

leave_comment = function(elem) {
   console.log("comment")
   let author = $(elem).parents()[1].children[0].children[0].value
   let title = $(elem).parents()[1].children[0].children[1].value
   let comment = $(elem).siblings()[0].value
   let div = document.createElement('div');
   div.className = "comment";

   if (comment.length > 0) {
       let csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
       $.ajax({
           url: `/feed/leave_comment/${title}/${author}`,
           type: 'POST',
           data: {comment: comment},
           success: function(data){
               if (data['added']) {
                   div.innerHTML = `<h5 style=\"margin-left: 10px; padding: 0\">${data['author']}:<br/>  ${comment}</h5>`;
                   $(elem).parents()[1].children[3].appendChild(div) }
               },
           beforeSend: function (xhr) {
               xhr.setRequestHeader("X-CSRFToken", `${csrf_token}`);
           },
           dataType: 'json',
       });
   }
}
