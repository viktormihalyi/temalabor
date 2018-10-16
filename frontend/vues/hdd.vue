<template>
    <div>                               
        <h5 style="margin-top:25px">Kapacitás</h5>
        <div class="input-group mb-3">
            <input type="number" class="form-control" placeholder="Minimum" name="sizeFrom">
            <div class="input-group-prepend">
                <span class="input-group-text"> - </span>
            </div>
            <input type="number" class="form-control" placeholder="Maximum" name="sizeTo">
        </div>
        
        <h5 style="margin-top:25px">Fordulatszám</h5>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="hddRpm0" name="hddRpm" value="5400">
            <label class="custom-control-label" for="hddRpm0">5400 rpm</label>
        </div>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="hddRpm1" name="hddRpm" value="7200">
            <label class="custom-control-label" for="hddRpm1">7200 rpm</label>
        </div>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="hddRpm2" name="hddRpm" value="10000">
            <label class="custom-control-label" for="hddRpm2">10000 rpm</label>
        </div>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="hddRpm3" name="hddRpm" value="15000">
            <label class="custom-control-label" for="hddRpm3">15000 rpm</label>
        </div>

        <h5 style="margin-top:25px">Átmérő</h5>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" id="hddSize0" name="hddSize" value="2.5">
            <label class="custom-control-label" for="hddSize0">2,5 inch</label>
        </div>  
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" id="hddSize1" name="hddSize" value="3.5">
            <label class="custom-control-label" for="hddSize1">3,5 inch</label>
        </div>
    </div>
</template>