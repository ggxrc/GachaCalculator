package com.ads.dorisolucoes

import android.os.Bundle
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class MainActivity : AppCompatActivity() {

    private lateinit var continuar_btn : Button
    private var item_selecionado : View? = null
    private var servico_selecionado : Servico? = null


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        carregarServicos()

    }
    private fun carregarServicos(){
        val containerServicos = findViewById<LinearLayout>(R.id.containerServicos)
        val servicos = ServicosRepository.getServicos()

        // 3. Para cada serviço, criar e adicionar a view
        servicos.forEach { servico ->
            val itemView = criarItemServico(servico, containerServicos)
            containerServicos.addView(itemView)
        }
    }
    private fun criarItemServico(servico: Servico, parent: ViewGroup): View {

        val itemView = layoutInflater.inflate(R.layout.item_servico, parent, false)

        val ivImagem = itemView.findViewById<ImageView>(R.id.ivServicoImagem)
        val tvNome = itemView.findViewById<TextView>(R.id.tvServicoNome)
        val tvDescricao = itemView.findViewById<TextView>(R.id.tvServicoDescricao)
        continuar_btn = findViewById(R.id.continuar)

        ivImagem.setImageResource(servico.imagemId)
        tvNome.text = servico.nome
        tvDescricao.text = servico.desc

        itemView.setOnClickListener {
            // 1. Remove destaque do item anterior
            item_selecionado?.setBackgroundResource(R.drawable.bg_servico)

            // 2. Destaca o item clicado
            itemView.setBackgroundResource(R.drawable.bg_servico_selecionado)

            // 3. Guarda qual item está selecionado
            item_selecionado = itemView

            when (item_selecionado?.id){
                TODO() -> TODO()
            }

            Toast.makeText(this, "Selecionou: ${servico.nome}", Toast.LENGTH_SHORT).show()
        }

        return itemView
    }
}