const forgotBtn = document.getElementById('forgotBtn');
const btnSubmit = document.getElementById('loginForm');
const divAlert = document.getElementById('div-alert');
const csrfToken = getCsrfToken();
if (btnSubmit) {
    btnSubmit.addEventListener('submit', async (e) => {
        e.preventDefault();
        const emailInput = document.getElementById('EmailInput').value;
        const passwordInput = document.getElementById('PasswordInput').value;
        let data = {
            email: emailInput,
            password: passwordInput
        };
        try {
            const result = await axios.post('/user/check-login', data, {
                headers: {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": csrfToken
                }
            });
            if (result.data.message === 'success') {
                const token = result.data.token;
                localStorage.setItem('token', token);
            
                if (result.data.role === 'admin') {
                    await displayNotification('Login Successful as Admin', 'success', divAlert);
                    window.location.href = '/new_dashboard'; 
                } else {
                    await displayNotification('Login Successful', 'success', divAlert);
                    window.location.href = '/expense/MainHome'; 
                }
            }
        } catch (error) {
            if (error.response.data.message) {
                if (error.response.data.message == 'Failed') {
                    await displayNotification("Invalid Credentials!", 'warning', divAlert);
                } else if (error.response.data.message === 'NotExist') {
                    await displayNotification("User not exist please register yourself first!", 'warning', divAlert);
                }
                else {
                    await displayNotification(error.response.data.message, 'danger', divAlert);
                }
            }
            else {
                await displayNotification("Internal Server Error!", 'danger', divAlert);
            }
        }
    });
}
if (forgotBtn) {
    forgotBtn.addEventListener('click', async (e) => {
        const emailId = document.getElementById('EmailId').value;
        if (emailId == '') {
            await displayNotification('Please Enter Valid Email Address!', 'warning', divAlert);
        } else {
            try {
                const response = await axios.post('/user/send-forget-password-link/', { emailId }
                );
                if (response.data.message == 'success') {
                    $('#forgotPasswordModal').modal('hide');
                    await displayNotification('Email Sent successfully check the email for further instructions!', 'success', divAlert);
                    window.location.reload();
                }
            } catch (error) {
                if (error.response.data.status === 404) {
                    $('#forgotPasswordModal').modal('hide');
                    await displayNotification(error.response.data.message, 'danger', divAlert);
                } else {
                    $('#forgotPasswordModal').modal('hide');
                    await displayNotification(error.response.data.message, 'danger', divAlert);
                }
                if (error.response.data.status) { }
                else {
                    await displayNotification("Internal Server Error!", 'danger', divAlert);
                }
            }
        }
    })
}
function displayNotification(message, type, container) {
    return new Promise((resolve) => {
        const notificationDiv = document.createElement('div');
        notificationDiv.className = `alert alert-${type}`;
        notificationDiv.textContent = message;
        container.appendChild(notificationDiv);
        setTimeout(() => {
            notificationDiv.remove();
            resolve();
        }, 2000);
    });
}
