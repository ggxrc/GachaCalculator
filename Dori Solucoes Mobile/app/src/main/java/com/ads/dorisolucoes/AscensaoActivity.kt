package com.ads.dorisolucoes

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Spinner
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity

data class ItensColetados(
    val drop_cinza: Int,
    val drop_verde: Int,
    val drop_raro: Int,
    val drop_boss: Int,
    val pedra_azul: Int,
    val pedra_roxa: Int,
    val pedra_dourada: Int,
    val item_coletado: Int
)

class AscensaoActivity : AppCompatActivity() {

    private lateinit var continuarButton: Button
    private lateinit var spinnerNivelAtual: Spinner
    private lateinit var spinnerNivelDesejado: Spinner

    val personagensDificuldade = mapOf(
        1 to listOf("Ifa", "Kazuha", "Emillie", "Kaveh", "Kachina", "Noelle", "Furina", "Fischl", "Bennett"),
        2 to listOf("Scaramouche", "Chasca", "Jean", "Lynette", "Sucrose", "Yumemizuki Mizuki", "Kinich", "Kirara", "Tighnari", "Chiori", "Xilonen", "Dahlia", "Layla", "Dori", "Iansan", "Lisa", "Yae Miko", "Chevreuse", "Mavuika"),
        3 to listOf("Faruzan", "Lan Yan", "Sayu", "Retentora", "Collei", "Nahida", "Yaoyao", "Ningguang", "Yunjin", "Candace", "Mualani", "Neuvillette", "Nilou", "Xingqiu", "Yelan", "Citlali", "Diona", "Escoffier", "Kaeya", "Rosaria", "Skirk", "Kujou Sara", "Kuki Shinobu", "Ororon", "Varesa", "Amber", "Gaming", "Lyney", "Xiangling", "Yoimiya"),
        4 to listOf("Venti", "Xiao", "Alhaitham", "Albedo", "Gorou", "Navia", "Zhongli", "Barbara", "Mona", "Kokomi", "Sigewinne", "Childe", "Charlotte", "Eula", "Freminet", "Ganyu", "Ayaka", "Mica", "Shenhe", "Wriothesley", "Beidou", "Clorinde", "Razor", "Raiden Shogun", "Arlecchino", "Dehya", "Diluc", "Hu tao", "Klee", "Thoma", "Yanfei"),
        5 to listOf("Heizou", "Baizhu", "Itto", "Ayato", "Aloy", "Chongyun", "Qiqi", "Cyno", "Keqing", "Sethos", "Xinyan")
    ).flatMap { (dificuldade, personagens) ->
        personagens.map { it to dificuldade }
    }.toMap()

    val itens_necessarios = mapOf(
        "Lvl 1 - 20+" to mapOf(
            "pedra_azul" to 0,
            "pedra_roxa" to 0,
            "pedra_dourada" to 0,
            "item_boss" to 0,
            "item_coleta" to 3,
            "drop_cinza" to 3,
            "drop_verde" to 0,
            "drop_raro" to 0
        ),
        "Lvl 20 - 40+" to mapOf(
            "pedra_azul" to 3,
            "pedra_roxa" to 0,
            "pedra_dourada" to 0,
            "item_boss" to 2,
            "item_coleta" to 10,
            "drop_cinza" to 15,
            "drop_verde" to 0,
            "drop_raro" to 0
        ),
        "Lvl 40 - 50+" to mapOf(
            "pedra_azul" to 6,
            "pedra_roxa" to 0,
            "pedra_dourada" to 0,
            "item_boss" to 4,
            "item_coleta" to 20,
            "drop_cinza" to 0,
            "drop_verde" to 12,
            "drop_raro" to 0
        ),
        "Lvl 50 - 60+" to mapOf(
            "pedra_azul" to 0,
            "pedra_roxa" to 3,
            "pedra_dourada" to 0,
            "item_boss" to 8,
            "item_coleta" to 30,
            "drop_cinza" to 0,
            "drop_verde" to 18,
            "drop_raro" to 0
        ),
        "Lvl 60 - 70+" to mapOf(
            "pedra_azul" to 0,
            "pedra_roxa" to 6,
            "pedra_dourada" to 0,
            "item_boss" to 12,
            "item_coleta" to 45,
            "drop_cinza" to 0,
            "drop_verde" to 0,
            "drop_raro" to 12
        ),
        "Lvl 70 - 80+" to mapOf(
            "pedra_azul" to 0,
            "pedra_roxa" to 0,
            "pedra_dourada" to 6,
            "item_boss" to 20,
            "item_coleta" to 60,
            "drop_cinza" to 0,
            "drop_verde" to 0,
            "drop_raro" to 24
        )
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_ascencao)
        continuarButton = findViewById(R.id.resultado)

        continuarButton.setOnClickListener {
            calcularAscensao()
        }
    }

    private fun verificaVazios(lista_ids: ItensColetados): Boolean {
        for (id in lista_ids.toString().toList()){
            if (id.isWhitespace())
                AlertDialog.Builder(this)
                    .setTitle("Atenção")
                    .setMessage("Por favor, preencha todos os campos.")
                    .setPositiveButton("OK") { _, _ -> }
                    .show()
                return false
        }
        return true
    }

    fun calcularAscensao() {
        val preco_base = 30.0

        val nivelAtual = findViewById<Spinner>(R.id.spinnerNivelAtual).selectedItem.toString()
        val nivelDesejado = findViewById<Spinner>(R.id.spinnerNivelDesejado).selectedItem.toString()

        val lista_itens = ItensColetados(
            findViewById<EditText>(R.id.etDropCinza).text.toString().toIntOrNull() ?: 0,
            findViewById<EditText>(R.id.etDropVerde).text.toString().toIntOrNull() ?: 0,
            findViewById<EditText>(R.id.etDropRaro).text.toString().toIntOrNull() ?: 0,
            findViewById<EditText>(R.id.etBoss).text.toString().toIntOrNull() ?: 0,
            findViewById<EditText>(R.id.etPedraAzul).text.toString().toIntOrNull() ?: 0,
            findViewById<EditText>(R.id.etPedraRoxa).text.toString().toIntOrNull() ?: 0,
            findViewById<EditText>(R.id.etPedraDourada).text.toString().toIntOrNull() ?: 0,
            findViewById<EditText>(R.id.etColeta).text.toString().toIntOrNull() ?: 0
        )
        if (!verificaVazios(lista_itens))
            return
    }
}