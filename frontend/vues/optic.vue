<template>
    <div>                               
        <h5 style="margin-top:25px">Típus</h5>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="oddtype0" name="oddtype" value="cd">
            <label class="custom-control-label" for="oddtype0">Cd író/olvasó</label>
        </div>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="oddtype1" name="oddtype" value="dvd">
            <label class="custom-control-label" for="oddtype1">DVD író/olvasó</label>
        </div>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="oddtype2" name="oddtype" value="bluray">
            <label class="custom-control-label" for="oddtype2">Blu-ray író/olvasó</label>
        </div>

        <h5 style="margin-top:25px">Kialakítás</h5>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" id="oddkind0" name="oddkind" value="internal">
            <label class="custom-control-label" for="oddkind0">Belső</label>
        </div>  
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" id="oddkind1" name="oddkind" value="external">
            <label class="custom-control-label" for="oddkind1">Külső</label>
        </div>
    </div>
</template>