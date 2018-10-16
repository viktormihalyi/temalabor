<template>
    <div>                               
        <h5 style="margin-top:25px">Kapacitás</h5>
        <div class="input-group mb-3">
            <input type="number" class="form-control" placeholder="Minimum" name="minCapac">
            <div class="input-group-prepend">
                <span class="input-group-text"> - </span>
            </div>
            <input type="number" class="form-control" placeholder="Maximum" name="maxCapac">
        </div>
        
        <h5 style="margin-top:25px">NAND flash típusa</h5>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="ssdNandType0" name="ssdNandType" value="slc">
            <label class="custom-control-label" for="ssdNandType0">SLC</label>
        </div>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="ssdNandType1" name="ssdNandType" value="mlc">
            <label class="custom-control-label" for="ssdNandType1">MLC</label>
        </div>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="ssdNandType2" name="ssdNandType" value="tlc">
            <label class="custom-control-label" for="ssdNandType2">TLC</label>
        </div>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="ssdNandType3" name="ssdNandType" value="3d XPoint">
            <label class="custom-control-label" for="ssdNandType3">3D XPoint</label>
        </div>

        <h5 style="margin-top:25px">Típus</h5>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" id="ssdtype0" name="ssdtype" value="2.5">
            <label class="custom-control-label" for="ssdtype0">2,5 inch</label>
        </div>  
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" id="ssdtype1" name="ssdtype" value="M.2">
            <label class="custom-control-label" for="ssdtype1">M.2</label>
        </div>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" id="ssdtype2" name="ssdtype" value="NVMe">
            <label class="custom-control-label" for="ssdtype2">NVMe</label>
        </div>
    </div>
</template>