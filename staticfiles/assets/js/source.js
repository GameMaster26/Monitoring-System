document.addEventListener('DOMContentLoaded', function() {
    const sourceOfExposureField = document.querySelector('#id_source_of_exposure');
    const otherAnimalFieldWrapper = document.querySelector('#div_id_other_animal');

    function toggleOtherAnimalField() {
        if (sourceOfExposureField.value === 'Others') {
            otherAnimalFieldWrapper.style.display = 'block';
        } else {
            otherAnimalFieldWrapper.style.display = 'none';
        }
    }

    sourceOfExposureField.addEventListener('change', toggleOtherAnimalField);
    toggleOtherAnimalField();  // Initial call to set the correct state
});
