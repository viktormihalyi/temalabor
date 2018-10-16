<template> 
    <div>
        <h5 style="margin-top:25px">Méret szabvány</h5>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="size0" name="size" value="ATX">
            <label class="custom-control-label" for="size0">ATX</label>
        </div>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="size1" name="size" value="micro-ATX">
            <label class="custom-control-label" for="size1">micro-ATX</label>
        </div>
        <div class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" id="size2" name="size" value="mini-ITX">
            <label class="custom-control-label" for="size2">mini-ITX</label>
        </div>

        <h5 style="margin-top:25px">Memória típusa</h5>
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" id="memtip0" name="memtip" value="DDR3">
            <label class="custom-control-label" for="memtip0">DDR3</label>
        </div>  
        <div class="custom-control custom-radio">
            <input type="radio" class="custom-control-input" id="memtip1" name="memtip" value="DDR4">
            <label class="custom-control-label" for="memtip1">DDR4</label>
        </div>
    </div>
</template>