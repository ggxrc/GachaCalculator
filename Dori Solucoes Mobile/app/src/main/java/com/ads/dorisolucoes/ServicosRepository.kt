package com.ads.dorisolucoes

object ServicosRepository {
    fun getServicos() : List<Servico>{
        return listOf(
            Servico(
                nome = "Exploração",
                imagemId = R.drawable.dori_chibi_money,
                desc = "Precisa de gemas? então vamos abrir uns baús 👌",
                destino = ExploracaoActivity::class.java
            ),
            Servico(
                nome = "Ascensão",
                imagemId = R.drawable.dori_hug,
                desc = "O serviço de Ascenção se encontra indisponível no momento 🥲",
                destino = null
            ),
            Servico(
                nome = "Builds",
                imagemId = R.drawable.dori_chibi_oksign,
                desc = "Em Breve... Fique ligado!",
                destino = null
            )
        )
    }
}