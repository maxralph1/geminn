let tabList = document.querySelectorAll('#edit_product_specification_tab');
let formList = document.querySelectorAll('#edit_product_specification_form');

let addTabList = document.querySelectorAll('#add_product_specification_tab');
let addFormList = document.querySelectorAll('#add_product_specification_form');

let editImageTabList = document.querySelectorAll('#edit_image_tab');
let editImageFormList = document.querySelectorAll('#edit_image_form');

document.addEventListener('DOMContentLoaded', () => {
        formList.forEach(form => {
            form.classList.add('d-none')
        }, false);
        addFormList.forEach(addForm => {
            addForm.classList.add('d-none')
        }, false);
        editImageFormList.forEach(editImageForm => {
            editImageForm.classList.add('d-none')
        }, false);
});

tabList.forEach(tab => tab.addEventListener('click', (e) => {
    e.preventDefault()
        formList.forEach(form => {
            if (form.classList.contains('d-none')) {
                form.classList.remove('d-none')
            } else {
                form.classList.add('d-none')
            }
        })
    })
);

addTabList.forEach(addTab => addTab.addEventListener('click', (e) => {
    e.preventDefault()
        addFormList.forEach(addForm => {
            if (addForm.classList.contains('d-none')) {
                addForm.classList.remove('d-none')
            } else {
                addForm.classList.add('d-none')
            }
        })
    })
);

editImageTabList.forEach(editImageTab => editImageTab.addEventListener('click', (e) => {
        e.preventDefault()
        editImageFormList.forEach(editImageForm => {
            if (editImageForm.classList.contains('d-none')) {
                editImageForm.classList.remove('d-none')
            } else {
                editImageForm.classList.add('d-none')
            }
        })
    })
);


