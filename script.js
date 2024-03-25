// static/script.js

document.addEventListener("DOMContentLoaded",function () {
  // Handle form submission via AJAX
  function handleFormSubmit(formClass) {
    const forms = document.querySelectorAll("." + formClass);

    forms.forEach((form) => {
      form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent the default form submission behavior

        // Fetch API to submit the form data asynchronously
        fetch(form.action, {
          method: form.method,
          body: new FormData(form),
          headers: {
            Accept: "application/json",
          },
        })
          .then((response) => response.json())
          .then((data) => {
            // Handle the response if needed

            // Optionally, update the content on the page without a full reload
            // For example, you can update a table or display a success message
            // depending on the form submitted.
            console.log("Form submitted successfully:", data);

            // Add logic to update the content on the page as needed
            // For example, you can redirect to the index page after submission:
            // window.location.href = "/";
          })
          .catch((error) => {
            console.error("Error submitting form:", error);
          });
      });
    });
  }

  // Call the function for forms with the specified class
  handleFormSubmit("ajax-form");
});
