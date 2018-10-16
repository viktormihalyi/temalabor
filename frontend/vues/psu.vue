<template>
    <div>                               
        <h5 style="margin-top:25px">Teljesítmény</h5>
        <div class="input-group mb-3">
            <input type="number" class="form-control" placeholder="Minimum" name="minPerform">
            <div class="input-group-prepend">
                <span class="input-group-text"> - </span>
            </div>
            <input type="number" class="form-control" placeholder="Maximum" name="maxPerform">
        </div>
        
        <h5 style="margin-top:25px">Kábelezés</h5>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="cable2" name="cable" value="fix">
            <label class="custom-control-label" for="cable2">Fix kábelezésű</label>
        </div>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="cable1" name="cable" value="halfmodular">
            <label class="custom-control-label" for="cable1">Félmoduláris</label>
        </div>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="cable0" name="cable" value="modular">
            <label class="custom-control-label" for="cable0">Moduláris</label>
        </div>
    </div>
</template>