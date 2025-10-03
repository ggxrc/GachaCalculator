package com.ads.dorisolucoes

data class Servico(
    val nome : String,
    val imagemId : Int,
    val desc : String,
    val destino : Class<*>?// atributo que guarda o destino do serviço em questão. Por causa do serviço de Builds que é propositalmente feito pra não ter caminho, o destino pode receber null.
)
