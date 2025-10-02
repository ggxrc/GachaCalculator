package com.ads.dorisolucoes

data class Servico(
    val nome : String,
    val imagemId : Int,
    val desc : String,
    val destino : Class<*> // atributo que guarda o destino do serviço em questão.
)
