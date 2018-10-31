<template>
    <div>
        <center><button class="btn btn-primary" style="margin:25px">Találatok szűrése</button></center>
        <h5>Keresés</h5>
        <input type="text" name="searched" class="form-control" id="searchedText">
        <h5 style="margin-top:25px">Ár</h5>
        <div class="input-group mb-3">
            <input type="number" name="priceFrom" class="form-control" placeholder="Minimum">
            <div class="input-group-prepend">
                <span class="input-group-text"> - </span>
            </div>
            <input type="number" name="priceTo" class="form-control" placeholder="Maximum">
        </div>
    </div>
</template>