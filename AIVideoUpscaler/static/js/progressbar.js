const uploadForm=document.getElementById('uploadForm')
const uploadBtn=document.getElementById('uploadBtnSubmit')
const input=document.getElementById('inputGroupFile02')
const progressDiv=document.getElementById('uploadProgress')
const cancelBtn=document.getElementById('cancelBtn')
const csrf=document.getElementsByName('csrfmiddlewaretoken')
input.addEventListener('change',()=>{
    progressDiv.classList.remove("invisible")
    cancelBtn.classList.remove("invisible")
    const video_data=input.files[0]
    // alert(video_data)
    const fd=new FormData()
    fd.append('csrfmiddlewaretoken',csrf[0].value)
    fd.append('videodata',video_data)
    $.ajax({
        type:'POST',
        url: uploadForm.action,
        enctype: 'multipart/form-data',
        data: fd,
        beforeSend: function(){
            console.log('before')
            // alertBox.innerHTML= ""
            // imageBox.innerHTML = ""
        },
        xhr: function(){
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress', e=>{
                // console.log(e)
                if (e.lengthComputable) {
                    progressDiv.classList.remove('invisible')
                    var percent = e.loaded / e.total * 100
                    percent=percent.toFixed(1);
                    if(percent==100){
                        uploadBtn.classList.remove("disabled")
                    }
                    // console.log(percent)

                    progressDiv.innerHTML = `<div class="progress-bar" role="progressbar" style="width: ${percent}%" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100">${percent}%</div>
                                           `
                }

            })
            cancelBtn.addEventListener('click', ()=>{
                xhr.abort()
                setTimeout(()=>{
                    uploadForm.reset()
                    progressDiv.classList.add('invisible')
                    // alertBox.innerHTML = ""
                    cancelBtn.classList.add('invisible')
                    uploadBtn.classList.add('disabled')
                }, 2000)
            })
            return xhr
        },
        success: function(response){
            console.log(response)
            // imageBox.innerHTML = `<img src="${url}" width="300px">`
            // alertBox.innerHTML = `<div class="alert alert-success" role="alert">
            //                         Successfully uploaded the image below
            //                     </div>`
            // cancelBtn.classList.add('invisible')
        },
        error: function(error){
            console.log(error)
            // alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
            //                         Ups... something went wrong
            //                     </div>`
        },
        cache: false,
        contentType: false,
        processData: false,
    })
})
