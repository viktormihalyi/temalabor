<template>
    <div>                               
        <h5 style="margin-top:25px">Felépítés</h5>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="buildtype0" name="buildtype" value="water">
            <label class="custom-control-label" for="buildtype0">Vízhűtés</label>
        </div>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="buildtype1" name="buildtype" value="active">
            <label class="custom-control-label" for="buildtype1">Aktív</label>
        </div>

        <h5 style="margin-top:25px">Típus</h5>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="coolertype0" name="coolertype" value="case">
            <label class="custom-control-label" for="coolertype0">Ház</label>
        </div>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="coolertype1" name="coolertype" value="processor">
            <label class="custom-control-label" for="coolertype1">Processzor</label>
        </div>
    </div>
</template>