#!/usr/bin/python3
tldList = {
'all':['.aaa', '.aarp', '.abarth', '.abb', '.abbott', '.abbvie', '.abc', '.able', '.abogado', '.abudhabi', '.ac', '.academy', '.accenture', '.accountant', '.accountants', '.aco', '.active', '.actor', '.ad', '.adac', '.ads', '.adult', '.ae', '.co.ae', '.net.ae', '.aeg', '.aero', '.airport.aero', '.cargo.aero', '.charter.aero', '.aetna', '.af', '.com.af', '.net.af', '.org.af', '.afamilycompany', '.afl', '.africa', '.ag', '.co.ag', '.com.ag', '.net.ag', '.nom.ag', '.org.ag', '.agakhan', '.agency', '.ai', '.com.ai', '.net.ai', '.off.ai', '.org.ai', '.aig', '.aigo', '.airbus', '.airforce', '.airtel', '.akdn', '.al', '.com.al', '.net.al', '.org.al', '.alfaromeo', '.alibaba', '.alipay', '.allfinanz', '.allstate', '.ally', '.alsace', '.alstom', '.am', '.co.am', '.com.am', '.net.am', '.north.am', '.org.am', '.radio.am', '.south.am', '.amazon', '.americanexpress', '.americanfamily', '.amex', '.amfam', '.amica', '.amsterdam', '.an', '.analytics', '.android', '.anquan', '.anz', '.ao', '.co.ao', '.it.ao', '.og.ao', '.pb.ao', '.aol', '.apartments', '.app', '.apple', '.aq', '.aquarelle', '.ar', '.com.ar', '.int.ar', '.net.ar', '.org.ar', '.arab', '.aramco', '.archi', '.army', '.arpa', '.art', '.arte', '.as', '.asda', '.asia', '.associates', '.at', '.co.at', '.or.at', '.athleta', '.attorney', '.au', '.asn.au', '.com.au', '.id.au', '.info.au', '.net.au', '.org.au', '.auction', '.audi', '.audible', '.audio', '.auspost', '.author', '.auto', '.autos', '.avianca', '.aw', '.aws', '.ax', '.axa', '.az', '.biz.az', '.co.az', '.com.az', '.edu.az', '.info.az', '.int.az', '.mil.az', '.name.az', '.net.az', '.org.az', '.pp.az', '.pro.az', '.azure', '.ba', '.co.ba', '.baby', '.baidu', '.banamex', '.bananarepublic', '.band', '.bank', '.bar', '.barcelona', '.barclaycard', '.barclays', '.barefoot', '.bargains', '.baseball', '.basketball', '.bauhaus', '.bayern', '.bb', '.com.bb', '.net.bb', '.org.bb', '.bbc', '.bbt', '.bbva', '.bcg', '.bcn', '.bd', '.ac.bd', '.com.bd', '.net.bd', '.org.bd', '.be', '.beats', '.beauty', '.beer', '.bentley', '.berlin', '.best', '.bestbuy', '.bet', '.bf', '.bg', '.bh', '.com.bh', '.bharti', '.bi', '.co.bi', '.com.bi', '.edu.bi', '.info.bi', '.mo.bi', '.net.bi', '.or.bi', '.org.bi', '.bible', '.bid', '.bike', '.bing', '.bingo', '.bio', '.biz', '.auz.biz', '.bj', '.com.bj', '.bl', '.black', '.blackfriday', '.blanco', '.blockbuster', '.blog', '.bloomberg', '.blue', '.bm', '.com.bm', '.net.bm', '.org.bm', '.bms', '.bmw', '.bn', '.com.bn', '.bnl', '.bnpparibas', '.bo', '.com.bo', '.net.bo', '.org.bo', '.tv.bo', '.boats', '.boehringer', '.bofa', '.bom', '.bond', '.boo', '.book', '.booking', '.boots', '.bosch', '.bostik', '.boston', '.bot', '.boutique', '.box', '.bq', '.br', '.abc.br', '.adm.br', '.adv.br', '.agr.br', '.am.br', '.aparecida.br', '.arq.br', '.art.br', '.ato.br', '.belem.br', '.bhz.br', '.bio.br', '.blog.br', '.bmd.br', '.boavista.br', '.bsb.br', '.campinas.br', '.caxias.br', '.cim.br', '.cng.br', '.cnt.br', '.com.br', '.coop.br', '.curitiba.br', '.ecn.br', '.eco.br', '.emp.br', '.eng.br', '.esp.br', '.etc.br', '.eti.br', '.far.br', '.flog.br', '.floripa.br', '.fm.br', '.fnd.br', '.fortal.br', '.fot.br', '.foz.br', '.fst.br', '.g12.br', '.ggf.br', '.gru.br', '.imb.br', '.ind.br', '.inf.br', '.jampa.br', '.jor.br', '.lel.br', '.macapa.br', '.maceio.br', '.manaus.br', '.mat.br', '.med.br', '.mil.br', '.mus.br', '.natal.br', '.net.br', '.nom.br', '.not.br', '.ntr.br', '.odo.br', '.org.br', '.palmas.br', '.poa.br', '.ppg.br', '.pro.br', '.psc.br', '.psi.br', '.qsl.br', '.radio.br', '.rec.br', '.recife.br', '.rio.br', '.salvador.br', '.sjc.br', '.slg.br', '.srv.br', '.taxi.br', '.teo.br', '.tmp.br', '.trd.br', '.tur.br', '.tv.br', '.vet.br', '.vix.br', '.vlog.br', '.wiki.br', '.zlg.br', '.bradesco', '.bridgestone', '.broadway', '.broker', '.brother', '.brussels', '.bs', '.com.bs', '.net.bs', '.org.bs', '.bt', '.com.bt', '.org.bt', '.budapest', '.bugatti', '.build', '.builders', '.business', '.buy', '.buzz', '.bv', '.bw', '.ac.bw', '.co.bw', '.net.bw', '.org.bw', '.by', '.com.by', '.minsk.by', '.net.by', '.bz', '.co.bz', '.com.bz', '.net.bz', '.org.bz', '.za.bz', '.bzh', '.ca', '.cab', '.cafe', '.cal', '.call', '.calvinklein', '.cam', '.camera', '.camp', '.cancerresearch', '.canon', '.capetown', '.capital', '.capitalone', '.car', '.caravan', '.cards', '.care', '.career', '.careers', '.cars', '.cartier', '.casa', '.case', '.caseih', '.cash', '.casino', '.cat', '.catering', '.catholic', '.cba', '.cbn', '.cbre', '.cbs', '.cc', '.edu.cc', '.org.cc', '.cd', '.com.cd', '.net.cd', '.org.cd', '.ceb', '.center', '.ceo', '.cern', '.cf', '.cfa', '.cfd', '.cg', '.ch', '.chanel', '.channel', '.charity', '.chase', '.chat', '.cheap', '.chintai', '.chloe', '.christmas', '.chrome', '.chrysler', '.church', '.ci', '.ac.ci', '.co.ci', '.com.ci', '.ed.ci', '.edu.ci', '.go.ci', '.in.ci', '.int.ci', '.net.ci', '.nom.ci', '.or.ci', '.org.ci', '.cipriani', '.circle', '.cisco', '.citadel', '.citi', '.citic', '.city', '.cityeats', '.ck', '.co.ck', '.net.ck', '.org.ck', '.cl', '.claims', '.cleaning', '.click', '.clinic', '.clinique', '.clothing', '.cloud', '.club', '.clubmed', '.cm', '.co.cm', '.com.cm', '.net.cm', '.cn', '.ac.cn', '.ah.cn', '.bj.cn', '.com.cn', '.cq.cn', '.fj.cn', '.gd.cn', '.gs.cn', '.gx.cn', '.gz.cn', '.ha.cn', '.hb.cn', '.he.cn', '.hi.cn', '.hk.cn', '.hl.cn', '.hn.cn', '.jl.cn', '.js.cn', '.jx.cn', '.ln.cn', '.mo.cn', '.net.cn', '.nm.cn', '.nx.cn', '.org.cn', '.qh.cn', '.sc.cn', '.sd.cn', '.sh.cn', '.sn.cn', '.sx.cn', '.tj.cn', '.tw.cn', '.xj.cn', '.xz.cn', '.yn.cn', '.zj.cn', '.co', '.com.co', '.net.co', '.nom.co', '.coach', '.codes', '.coffee', '.college', '.cologne', '.com', '.ae.com', '.africa.com', '.ar.com', '.br.com', '.cn.com', '.co.com', '.de.com', '.eu.com', '.gb.com', '.gr.com', '.hk.com', '.hu.com', '.jpn.com', '.kr.com', '.mex.com', '.no.com', '.nv.com', '.pty-ltd.com', '.qc.com', '.ru.com', '.sa.com', '.se.com', '.uk.com', '.us.com', '.uy.com', '.za.com', '.comcast', '.commbank', '.community', '.company', '.compare', '.computer', '.comsec', '.condos', '.construction', '.consulting', '.contact', '.contractors', '.cooking', '.cookingchannel', '.cool', '.coop', '.corsica', '.country', '.coupon', '.coupons', '.courses', '.cpa', '.cr', '.co.cr', '.ed.cr', '.fi.cr', '.go.cr', '.or.cr', '.sa.cr', '.credit', '.creditcard', '.creditunion', '.cricket', '.crown', '.crs', '.cruise', '.cruises', '.csc', '.cu', '.com.cu', '.cuisinella', '.cv', '.com.cv', '.int.cv', '.net.cv', '.nome.cv', '.org.cv', '.publ.cv', '.cw', '.com.cw', '.net.cw', '.cx', '.cy', '.ac.cy', '.biz.cy', '.com.cy', '.ekloges.cy', '.ltd.cy', '.name.cy', '.net.cy', '.org.cy', '.parliament.cy', '.press.cy', '.pro.cy', '.tm.cy', '.cymru', '.cyou', '.cz', '.co.cz', '.dabur', '.dad', '.dance', '.data', '.date', '.dating', '.datsun', '.day', '.dclk', '.dds', '.de', '.co.de', '.com.de', '.deal', '.dealer', '.deals', '.degree', '.delivery', '.dell', '.deloitte', '.delta', '.democrat', '.dental', '.dentist', '.desi', '.design', '.dev', '.dhl', '.diamonds', '.diet', '.digital', '.direct', '.directory', '.discount', '.discover', '.dish', '.diy', '.dj', '.dk', '.biz.dk', '.co.dk', '.dm', '.co.dm', '.com.dm', '.net.dm', '.org.dm', '.dnp', '.do', '.art.do', '.com.do', '.net.do', '.org.do', '.sld.do', '.web.do', '.docs', '.doctor', '.dodge', '.dog', '.doha', '.domains', '.doosan', '.dot', '.download', '.drive', '.dtv', '.dubai', '.duck', '.dunlop', '.duns', '.dupont', '.durban', '.dvag', '.dvr', '.dz', '.com.dz', '.earth', '.eat', '.ec', '.com.ec', '.fin.ec', '.info.ec', '.med.ec', '.net.ec', '.org.ec', '.pro.ec', '.eco', '.edeka', '.edu', '.education', '.ee', '.co.ee', '.com.ee', '.pri.ee', '.eg', '.com.eg', '.edu.eg', '.eun.eg', '.info.eg', '.name.eg', '.net.eg', '.org.eg', '.sci.eg', '.tv.eg', '.eh', '.email', '.emerck', '.energy', '.engineer', '.engineering', '.enterprises', '.epost', '.epson', '.equipment', '.er', '.ericsson', '.erni', '.es', '.com.es', '.edu.es', '.gob.es', '.nom.es', '.org.es', '.esq', '.estate', '.esurance', '.et', '.biz.et', '.com.et', '.info.et', '.name.et', '.net.et', '.org.et', '.etisalat', '.eu', '.eurovision', '.eus', '.events', '.everbank', '.exchange', '.expert', '.exposed', '.express', '.extraspace', '.fage', '.fail', '.fairwinds', '.faith', '.family', '.fan', '.fans', '.farm', '.farmers', '.fashion', '.fast', '.fedex', '.feedback', '.ferrari', '.ferrero', '.fi', '.fiat', '.fidelity', '.fido', '.film', '.final', '.finance', '.financial', '.fire', '.firestone', '.firmdale', '.fish', '.fishing', '.fit', '.fitness', '.fj', '.biz.fj', '.com.fj', '.info.fj', '.name.fj', '.net.fj', '.org.fj', '.pro.fj', '.fk', '.co.fk', '.flickr', '.flights', '.flir', '.florist', '.flowers', '.flsmidth', '.fly', '.fm', '.radio.fm', '.fo', '.foo', '.food', '.foodnetwork', '.football', '.ford', '.forex', '.forsale', '.forum', '.foundation', '.fox', '.fr', '.aeroport.fr', '.asso.fr', '.avocat.fr', '.chambagri.fr', '.chirurgiens-dentistes.fr', '.com.fr', '.experts-comptables.fr', '.geometre-expert.fr', '.gouv.fr', '.medecin.fr', '.nom.fr', '.notaires.fr', '.pharmacien.fr', '.port.fr', '.prd.fr', '.presse.fr', '.tm.fr', '.veterinaire.fr', '.free', '.fresenius', '.frl', '.frogans', '.frontdoor', '.frontier', '.ftr', '.fujitsu', '.fujixerox', '.fun', '.fund', '.furniture', '.futbol', '.fyi', '.ga', '.gal', '.gallery', '.gallo', '.gallup', '.game', '.games', '.gap', '.garden', '.gay', '.gb', '.gbiz', '.gd', '.gdn', '.ge', '.com.ge', '.edu.ge', '.mil.ge', '.net.ge', '.org.ge', '.pvt.ge', '.gea', '.gent', '.genting', '.george', '.gf', '.gg', '.co.gg', '.net.gg', '.org.gg', '.ggee', '.gh', '.com.gh', '.edu.gh', '.org.gh', '.gi', '.com.gi', '.gov.gi', '.ltd.gi', '.org.gi', '.gift', '.gifts', '.gives', '.giving', '.gl', '.co.gl', '.com.gl', '.edu.gl', '.net.gl', '.org.gl', '.glade', '.glass', '.gle', '.global', '.globo', '.gm', '.gmail', '.gmbh', '.gmo', '.gmx', '.gn', '.com.gn', '.gov.gn', '.net.gn', '.org.gn', '.godaddy', '.gold', '.goldpoint', '.golf', '.goo', '.goodhands', '.goodyear', '.goog', '.google', '.gop', '.got', '.gov', '.gp', '.com.gp', '.mobi.gp', '.net.gp', '.org.gp', '.gq', '.gr', '.com.gr', '.edu.gr', '.net.gr', '.org.gr', '.grainger', '.graphics', '.gratis', '.green', '.gripe', '.grocery', '.group', '.gs', '.gt', '.com.gt', '.net.gt', '.org.gt', '.gu', '.com.gu', '.guardian', '.gucci', '.guge', '.guide', '.guitars', '.guru', '.gw', '.gy', '.co.gy', '.com.gy', '.net.gy', '.hair', '.hamburg', '.hangout', '.haus', '.hbo', '.hdfc', '.hdfcbank', '.health', '.healthcare', '.help', '.helsinki', '.here', '.hermes', '.hgtv', '.hiphop', '.hisamitsu', '.hitachi', '.hiv', '.hk', '.com.hk', '.edu.hk', '.gov.hk', '.idv.hk', '.inc.hk', '.ltd.hk', '.net.hk', '.org.hk', '.公司.hk', '.hkt', '.hm', '.hn', '.com.hn', '.edu.hn', '.net.hn', '.org.hn', '.hockey', '.holdings', '.holiday', '.homedepot', '.homegoods', '.homes', '.homesense', '.honda', '.honeywell', '.horse', '.hospital', '.host', '.hosting', '.hot', '.hoteles', '.hotels', '.hotmail', '.house', '.how', '.hr', '.com.hr', '.hsbc', '.ht', '.adult.ht', '.art.ht', '.asso.ht', '.com.ht', '.edu.ht', '.firm.ht', '.info.ht', '.net.ht', '.org.ht', '.perso.ht', '.pol.ht', '.pro.ht', '.rel.ht', '.shop.ht', '.htc', '.hu', '.2000.hu', '.agrar.hu', '.bolt.hu', '.casino.hu', '.city.hu', '.co.hu', '.erotica.hu', '.erotika.hu', '.film.hu', '.forum.hu', '.games.hu', '.hotel.hu', '.info.hu', '.ingatlan.hu', '.jogasz.hu', '.konyvelo.hu', '.lakas.hu', '.media.hu', '.news.hu', '.org.hu', '.priv.hu', '.reklam.hu', '.sex.hu', '.shop.hu', '.sport.hu', '.suli.hu', '.szex.hu', '.tm.hu', '.tozsde.hu', '.utazas.hu', '.video.hu', '.hughes', '.hyatt', '.hyundai', '.ibm', '.icbc', '.ice', '.icu', '.id', '.biz.id', '.co.id', '.my.id', '.or.id', '.sch.id', '.web.id', '.ie', '.ieee', '.ifm', '.iinet', '.ikano', '.il', '.co.il', '.net.il', '.org.il', '.im', '.ac.im', '.co.im', '.com.im', '.ltd.co.im', '.net.im', '.org.im', '.plc.co.im', '.imamat', '.imdb', '.immo', '.immobilien', '.in', '.co.in', '.firm.in', '.gen.in', '.ind.in', '.net.in', '.org.in', '.inc', '.industries', '.infiniti', '.info', '.auz.info', '.ing', '.ink', '.institute', '.insurance', '.insure', '.int', '.intel', '.international', '.intuit', '.investments', '.io', '.ipiranga', '.iq', '.com.iq', '.ir', '.co.ir', '.irish', '.is', '.iselect', '.ismaili', '.ist', '.istanbul', '.it', '.abr.it', '.abruzzo.it', '.ag.it', '.agrigento.it', '.al.it', '.alessandria.it', '.alto-adige.it', '.altoadige.it', '.an.it', '.ancona.it', '.andria-barletta-trani.it', '.andria-trani-barletta.it', '.andriabarlettatrani.it', '.andriatranibarletta.it', '.ao.it', '.aosta.it', '.aoste.it', '.ap.it', '.aq.it', '.aquila.it', '.ar.it', '.arezzo.it', '.ascoli-piceno.it', '.ascolipiceno.it', '.asti.it', '.at.it', '.av.it', '.avellino.it', '.ba.it', '.balsan.it', '.bari.it', '.barletta-trani-andria.it', '.barlettatraniandria.it', '.bas.it', '.basilicata.it', '.belluno.it', '.benevento.it', '.bergamo.it', '.bg.it', '.bi.it', '.biella.it', '.bl.it', '.bn.it', '.bo.it', '.bologna.it', '.bolzano.it', '.bozen.it', '.br.it', '.brescia.it', '.brindisi.it', '.bs.it', '.bt.it', '.bz.it', '.ca.it', '.cagliari.it', '.cal.it', '.calabria.it', '.caltanissetta.it', '.cam.it', '.campania.it', '.campidano-medio.it', '.campidanomedio.it', '.campobasso.it', '.carbonia-iglesias.it', '.carboniaiglesias.it', '.carrara-massa.it', '.carraramassa.it', '.caserta.it', '.catania.it', '.catanzaro.it', '.cb.it', '.ce.it', '.cesena-forli.it', '.cesenaforli.it', '.ch.it', '.chieti.it', '.ci.it', '.cl.it', '.cn.it', '.co.it', '.como.it', '.cosenza.it', '.cr.it', '.cremona.it', '.crotone.it', '.cs.it', '.ct.it', '.cuneo.it', '.cz.it', '.dell-ogliastra.it', '.dellogliastra.it', '.emilia-romagna.it', '.emiliaromagna.it', '.emr.it', '.en.it', '.enna.it', '.fc.it', '.fe.it', '.fermo.it', '.ferrara.it', '.fg.it', '.fi.it', '.firenze.it', '.florence.it', '.fm.it', '.foggia.it', '.forli-cesena.it', '.forlicesena.it', '.fr.it', '.friuli-v-giulia.it', '.friuli-ve-giulia.it', '.friuli-vegiulia.it', '.friuli-venezia-giulia.it', '.friuli-veneziagiulia.it', '.friuli-vgiulia.it', '.friuliv-giulia.it', '.friulive-giulia.it', '.friulivegiulia.it', '.friulivenezia-giulia.it', '.friuliveneziagiulia.it', '.friulivgiulia.it', '.frosinone.it', '.fvg.it', '.ge.it', '.genoa.it', '.genova.it', '.go.it', '.gorizia.it', '.gr.it', '.grosseto.it', '.iglesias-carbonia.it', '.iglesiascarbonia.it', '.im.it', '.imperia.it', '.is.it', '.isernia.it', '.kr.it', '.la-spezia.it', '.laquila.it', '.laspezia.it', '.latina.it', '.laz.it', '.lazio.it', '.lc.it', '.le.it', '.lecce.it', '.lecco.it', '.li.it', '.lig.it', '.liguria.it', '.livorno.it', '.lo.it', '.lodi.it', '.lom.it', '.lombardia.it', '.lombardy.it', '.lt.it', '.lu.it', '.lucania.it', '.lucca.it', '.macerata.it', '.mantova.it', '.mar.it', '.marche.it', '.massa-carrara.it', '.massacarrara.it', '.matera.it', '.mb.it', '.mc.it', '.me.it', '.medio-campidano.it', '.mediocampidano.it', '.messina.it', '.mi.it', '.milan.it', '.milano.it', '.mn.it', '.mo.it', '.modena.it', '.mol.it', '.molise.it', '.monza-brianza.it', '.monza-e-della-brianza.it', '.monza.it', '.monzabrianza.it', '.monzaebrianza.it', '.monzaedellabrianza.it', '.ms.it', '.mt.it', '.na.it', '.naples.it', '.napoli.it', '.no.it', '.novara.it', '.nu.it', '.nuoro.it', '.og.it', '.ogliastra.it', '.olbia-tempio.it', '.olbiatempio.it', '.or.it', '.oristano.it', '.ot.it', '.pa.it', '.padova.it', '.padua.it', '.palermo.it', '.parma.it', '.pavia.it', '.pc.it', '.pd.it', '.pe.it', '.perugia.it', '.pesaro-urbino.it', '.pesarourbino.it', '.pescara.it', '.pg.it', '.pi.it', '.piacenza.it', '.piedmont.it', '.piemonte.it', '.pisa.it', '.pistoia.it', '.pmn.it', '.pn.it', '.po.it', '.pordenone.it', '.potenza.it', '.pr.it', '.prato.it', '.pt.it', '.pu.it', '.pug.it', '.puglia.it', '.pv.it', '.pz.it', '.ra.it', '.ragusa.it', '.ravenna.it', '.rc.it', '.re.it', '.reggio-calabria.it', '.reggio-emilia.it', '.reggiocalabria.it', '.reggioemilia.it', '.rg.it', '.ri.it', '.rieti.it', '.rimini.it', '.rm.it', '.rn.it', '.ro.it', '.roma.it', '.rome.it', '.rovigo.it', '.sa.it', '.salerno.it', '.sar.it', '.sardegna.it', '.sardinia.it', '.sassari.it', '.savona.it', '.si.it', '.sic.it', '.sicilia.it', '.sicily.it', '.siena.it', '.siracusa.it', '.so.it', '.sondrio.it', '.sp.it', '.sr.it', '.ss.it', '.suedtirol.it', '.sv.it', '.ta.it', '.taa.it', '.taranto.it', '.te.it', '.tempio-olbia.it', '.tempioolbia.it', '.teramo.it', '.terni.it', '.tn.it', '.to.it', '.torino.it', '.tos.it', '.toscana.it', '.tp.it', '.tr.it', '.trani-andria-barletta.it', '.trani-barletta-andria.it', '.traniandriabarletta.it', '.tranibarlettaandria.it', '.trapani.it', '.trentino-a-adige.it', '.trentino-aadige.it', '.trentino-alto-adige.it', '.trentino-altoadige.it', '.trentino-s-tirol.it', '.trentino-stirol.it', '.trentino-sud-tirol.it', '.trentino-sudtirol.it', '.trentino-sued-tirol.it', '.trentino-suedtirol.it', '.trentino.it', '.trentinoa-adige.it', '.trentinoaadige.it', '.trentinoalto-adige.it', '.trentinoaltoadige.it', '.trentinos-tirol.it', '.trentinosud-tirol.it', '.trentinosudtirol.it', '.trentinosued-tirol.it', '.trentinosuedtirol.it', '.trento.it', '.treviso.it', '.trieste.it', '.ts.it', '.turin.it', '.tuscany.it', '.tv.it', '.ud.it', '.udine.it', '.umb.it', '.umbria.it', '.urbino-pesaro.it', '.urbinopesaro.it', '.va.it', '.val-d-aosta.it', '.val-daosta.it', '.vald-aosta.it', '.valdaosta.it', '.valle-d-aosta.it', '.valle-daosta.it', '.valled-aosta.it', '.valledaosta.it', '.vao.it', '.varese.it', '.vb.it', '.vc.it', '.vda.it', '.ve.it', '.ven.it', '.veneto.it', '.venezia.it', '.venice.it', '.verbania.it', '.vercelli.it', '.verona.it', '.vi.it', '.vibo-valentia.it', '.vibovalentia.it', '.vicenza.it', '.viterbo.it', '.vr.it', '.vs.it', '.vt.it', '.vv.it', '.itau', '.itv', '.iveco', '.iwc', '.jaguar', '.java', '.jcb', '.jcp', '.je', '.co.je', '.net.je', '.org.je', '.jeep', '.jetzt', '.jewelry', '.jio', '.jlc', '.jll', '.jm', '.com.jm', '.jmp', '.jnj', '.jo', '.com.jo', '.name.jo', '.net.jo', '.org.jo', '.sch.jo', '.jobs', '.joburg', '.jot', '.joy', '.jp', '.akita.jp', '.co.jp', '.gr.jp', '.kyoto.jp', '.ne.jp', '.or.jp', '.osaka.jp', '.saga.jp', '.tokyo.jp', '.jpmorgan', '.jprs', '.juegos', '.juniper', '.kaufen', '.kddi', '.ke', '.ac.ke', '.co.ke', '.go.ke', '.info.ke', '.me.ke', '.mobi.ke', '.ne.ke', '.or.ke', '.sc.ke', '.kerryhotels', '.kerrylogistics', '.kerryproperties', '.kfh', '.kg', '.com.kg', '.net.kg', '.org.kg', '.kh', '.com.kh', '.edu.kh', '.net.kh', '.org.kh', '.ki', '.biz.ki', '.com.ki', '.edu.ki', '.gov.ki', '.info.ki', '.mobi.ki', '.net.ki', '.org.ki', '.phone.ki', '.tel.ki', '.kia', '.kim', '.kinder', '.kindle', '.kitchen', '.kiwi', '.km', '.nom.km', '.tm.km', '.kn', '.com.kn', '.koeln', '.komatsu', '.kosher', '.kp', '.kpmg', '.kpn', '.kr', '.co.kr', '.go.kr', '.ms.kr', '.ne.kr', '.or.kr', '.pe.kr', '.re.kr', '.seoul.kr', '.krd', '.kred', '.kuokgroup', '.kw', '.com.kw', '.edu.kw', '.net.kw', '.org.kw', '.ky', '.com.ky', '.net.ky', '.org.ky', '.kyoto', '.kz', '.com.kz', '.org.kz', '.la', '.lacaixa', '.ladbrokes', '.lamborghini', '.lamer', '.lancaster', '.lancia', '.lancome', '.land', '.landrover', '.lanxess', '.lasalle', '.lat', '.latino', '.latrobe', '.law', '.lawyer', '.lb', '.com.lb', '.edu.lb', '.net.lb', '.org.lb', '.lc', '.co.lc', '.com.lc', '.l.lc', '.net.lc', '.org.lc', '.p.lc', '.lds', '.lease', '.leclerc', '.lefrak', '.legal', '.lego', '.lexus', '.lgbt', '.li', '.liaison', '.lidl', '.life', '.lifeinsurance', '.lifestyle', '.lighting', '.like', '.lilly', '.limited', '.limo', '.lincoln', '.linde', '.link', '.lipsy', '.live', '.living', '.lixil', '.lk', '.com.lk', '.edu.lk', '.org.lk', '.llc', '.llp', '.loan', '.loans', '.locker', '.locus', '.loft', '.lol', '.london', '.lotte', '.lotto', '.love', '.lpl', '.lplfinancial', '.lr', '.com.lr', '.org.lr', '.ls', '.co.ls', '.net.ls', '.org.ls', '.lt', '.ltd', '.ltda', '.lu', '.lundbeck', '.lupin', '.luxe', '.luxury', '.lv', '.asn.lv', '.com.lv', '.conf.lv', '.edu.lv', '.id.lv', '.mil.lv', '.net.lv', '.org.lv', '.ly', '.com.ly', '.id.ly', '.med.ly', '.net.ly', '.org.ly', '.plc.ly', '.sch.ly', '.ma', '.ac.ma', '.co.ma', '.net.ma', '.org.ma', '.press.ma', '.macys', '.madrid', '.maif', '.maison', '.makeup', '.man', '.management', '.mango', '.map', '.market', '.marketing', '.markets', '.marriott', '.marshalls', '.maserati', '.mattel', '.mba', '.mc', '.asso.mc', '.tm.mc', '.mcd', '.mcdonalds', '.mckinsey', '.md', '.me', '.med', '.media', '.meet', '.melbourne', '.meme', '.memorial', '.men', '.menu', '.meo', '.merckmsd', '.metlife', '.mf', '.mg', '.co.mg', '.com.mg', '.mil.mg', '.net.mg', '.nom.mg', '.org.mg', '.prd.mg', '.tm.mg', '.mh', '.miami', '.microsoft', '.mil', '.mini', '.mint', '.mit', '.mitsubishi', '.mk', '.com.mk', '.edu.mk', '.inf.mk', '.name.mk', '.net.mk', '.org.mk', '.ml', '.mlb', '.mls', '.mm', '.biz.mm', '.com.mm', '.net.mm', '.org.mm', '.per.mm', '.mma', '.mn', '.mo', '.com.mo', '.net.mo', '.org.mo', '.mobi', '.mobile', '.mobily', '.moda', '.moe', '.moi', '.mom', '.monash', '.money', '.monster', '.montblanc', '.mopar', '.mormon', '.mortgage', '.moscow', '.moto', '.motorcycles', '.mov', '.movie', '.movistar', '.mp', '.mq', '.mr', '.edu.mr', '.org.mr', '.perso.mr', '.ms', '.co.ms', '.com.ms', '.org.ms', '.msd', '.mt', '.com.mt', '.net.mt', '.org.mt', '.mtn', '.mtpc', '.mtr', '.mu', '.ac.mu', '.co.mu', '.com.mu', '.net.mu', '.nom.mu', '.or.mu', '.org.mu', '.museum', '.mutual', '.mutuelle', '.mv', '.com.mv', '.mw', '.ac.mw', '.co.mw', '.com.mw', '.coop.mw', '.edu.mw', '.int.mw', '.net.mw', '.org.mw', '.mx', '.com.mx', '.edu.mx', '.gob.mx', '.net.mx', '.org.mx', '.my', '.com.my', '.mil.my', '.name.my', '.net.my', '.org.my', '.mz', '.co.mz', '.edu.mz', '.net.mz', '.org.mz', '.na', '.alt.na', '.co.na', '.com.na', '.edu.na', '.net.na', '.org.na', '.nab', '.nadex', '.nagoya', '.name', '.nationwide', '.natura', '.navy', '.nba', '.nc', '.asso.nc', '.nom.nc', '.ne', '.com.ne', '.info.ne', '.int.ne', '.org.ne', '.perso.ne', '.nec', '.net', '.auz.net', '.gb.net', '.hu.net', '.in.net', '.jp.net', '.ru.net', '.se.net', '.uk.net', '.netbank', '.netflix', '.network', '.neustar', '.new', '.newholland', '.news', '.next', '.nextdirect', '.nexus', '.nf', '.arts.nf', '.com.nf', '.firm.nf', '.info.nf', '.net.nf', '.org.nf', '.other.nf', '.per.nf', '.rec.nf', '.store.nf', '.web.nf', '.nfl', '.ng', '.com.ng', '.edu.ng', '.gov.ng', '.i.ng', '.lg.gov.ng', '.mobi.ng', '.name.ng', '.net.ng', '.org.ng', '.sch.ng', '.ngo', '.nhk', '.ni', '.ac.ni', '.biz.ni', '.co.ni', '.com.ni', '.edu.ni', '.gob.ni', '.in.ni', '.info.ni', '.int.ni', '.mil.ni', '.net.ni', '.nom.ni', '.org.ni', '.web.ni', '.nico', '.nike', '.nikon', '.ninja', '.nissan', '.nissay', '.nl', '.co.nl', '.com.nl', '.net.nl', '.no', '.co.no', '.fhs.no', '.folkebibl.no', '.fylkesbibl.no', '.gs.no', '.idrett.no', '.museum.no', '.priv.no', '.uenorge.no', '.vgs.no', '.nokia', '.northwesternmutual', '.norton', '.now', '.nowruz', '.nowtv', '.np', '.aero.np', '.asia.np', '.biz.np', '.com.np', '.coop.np', '.info.np', '.mil.np', '.mobi.np', '.museum.np', '.name.np', '.net.np', '.org.np', '.pro.np', '.travel.np', '.nr', '.biz.nr', '.com.nr', '.info.nr', '.net.nr', '.org.nr', '.nra', '.nrw', '.ntt', '.nu', '.co.nu', '.nyc', '.nz', '.ac.nz', '.co.net.nz', '.co.nz', '.geek.nz', '.gen.nz', '.iwi.nz', '.kiwi.nz', '.maori.nz', '.net.nz', '.org.nz', '.school.nz', '.obi', '.observer', '.off', '.office', '.okinawa', '.olayan', '.olayangroup', '.oldnavy', '.ollo', '.om', '.biz.om', '.co.om', '.com.om', '.med.om', '.mil.om', '.museum.om', '.net.om', '.org.om', '.pro.om', '.sch.om', '.omega', '.one', '.ong', '.onl', '.online', '.onyourside', '.ooo', '.open', '.oracle', '.orange', '.org', '.ae.org', '.hk.org', '.us.org', '.organic', '.orientexpress', '.origins', '.osaka', '.otsuka', '.ott', '.ovh', '.pa', '.abo.pa', '.com.pa', '.edu.pa', '.gob.pa', '.ing.pa', '.med.pa', '.net.pa', '.nom.pa', '.org.pa', '.sld.pa', '.page', '.pamperedchef', '.panasonic', '.panerai', '.paris', '.pars', '.partners', '.parts', '.party', '.passagens', '.pay', '.pccw', '.pe', '.com.pe', '.gob.pe', '.mil.pe', '.net.pe', '.nom.pe', '.org.pe', '.pet', '.pf', '.asso.pf', '.com.pf', '.org.pf', '.pfizer', '.pg', '.com.pg', '.net.pg', '.org.pg', '.ph', '.com.ph', '.net.ph', '.org.ph', '.pharmacy', '.phd', '.philips', '.phone', '.photo', '.photography', '.photos', '.physio', '.piaget', '.pics', '.pictet', '.pictures', '.pid', '.pin', '.ping', '.pink', '.pioneer', '.pizza', '.pk', '.biz.pk', '.com.pk', '.net.pk', '.org.pk', '.web.pk', '.pl', '.agro.pl', '.aid.pl', '.atm.pl', '.augustow.pl', '.auto.pl', '.babia-gora.pl', '.bedzin.pl', '.beskidy.pl', '.bialowieza.pl', '.bialystok.pl', '.bielawa.pl', '.bieszczady.pl', '.biz.pl', '.boleslawiec.pl', '.bydgoszcz.pl', '.bytom.pl', '.cieszyn.pl', '.com.pl', '.czeladz.pl', '.czest.pl', '.dlugoleka.pl', '.edu.pl', '.elblag.pl', '.elk.pl', '.glogow.pl', '.gmina.pl', '.gniezno.pl', '.gorlice.pl', '.grajewo.pl', '.gsm.pl', '.ilawa.pl', '.info.pl', '.jaworzno.pl', '.jelenia-gora.pl', '.jgora.pl', '.kalisz.pl', '.karpacz.pl', '.kartuzy.pl', '.kaszuby.pl', '.katowice.pl', '.kazimierz-dolny.pl', '.kepno.pl', '.ketrzyn.pl', '.klodzko.pl', '.kobierzyce.pl', '.kolobrzeg.pl', '.konin.pl', '.konskowola.pl', '.kutno.pl', '.lapy.pl', '.lebork.pl', '.legnica.pl', '.lezajsk.pl', '.limanowa.pl', '.lomza.pl', '.lowicz.pl', '.lubin.pl', '.lukow.pl', '.mail.pl', '.malbork.pl', '.malopolska.pl', '.mazowsze.pl', '.mazury.pl', '.media.pl', '.miasta.pl', '.mielec.pl', '.mielno.pl', '.mil.pl', '.mragowo.pl', '.naklo.pl', '.net.pl', '.nieruchomosci.pl', '.nom.pl', '.nowaruda.pl', '.nysa.pl', '.olawa.pl', '.olecko.pl', '.olkusz.pl', '.olsztyn.pl', '.opoczno.pl', '.opole.pl', '.org.pl', '.ostroda.pl', '.ostroleka.pl', '.ostrowiec.pl', '.ostrowwlkp.pl', '.pc.pl', '.pila.pl', '.pisz.pl', '.podhale.pl', '.podlasie.pl', '.polkowice.pl', '.pomorskie.pl', '.pomorze.pl', '.powiat.pl', '.priv.pl', '.prochowice.pl', '.pruszkow.pl', '.przeworsk.pl', '.pulawy.pl', '.radom.pl', '.rawa-maz.pl', '.realestate.pl', '.rel.pl', '.rybnik.pl', '.rzeszow.pl', '.sanok.pl', '.sejny.pl', '.sex.pl', '.shop.pl', '.sklep.pl', '.skoczow.pl', '.slask.pl', '.slupsk.pl', '.sos.pl', '.sosnowiec.pl', '.stalowa-wola.pl', '.starachowice.pl', '.stargard.pl', '.suwalki.pl', '.swidnica.pl', '.swiebodzin.pl', '.swinoujscie.pl', '.szczecin.pl', '.szczytno.pl', '.szkola.pl', '.targi.pl', '.tarnobrzeg.pl', '.tgory.pl', '.tm.pl', '.tourism.pl', '.travel.pl', '.turek.pl', '.turystyka.pl', '.tychy.pl', '.ustka.pl', '.walbrzych.pl', '.warmia.pl', '.warszawa.pl', '.waw.pl', '.wegrow.pl', '.wielun.pl', '.wlocl.pl', '.wloclawek.pl', '.wodzislaw.pl', '.wolomin.pl', '.wroclaw.pl', '.zachpomor.pl', '.zagan.pl', '.zarow.pl', '.zgora.pl', '.zgorzelec.pl', '.place', '.play', '.playstation', '.plumbing', '.plus', '.pm', '.pn', '.co.pn', '.net.pn', '.org.pn', '.pnc', '.pohl', '.poker', '.politie', '.porn', '.post', '.pr', '.biz.pr', '.com.pr', '.info.pr', '.isla.pr', '.name.pr', '.net.pr', '.org.pr', '.pro.pr', '.pramerica', '.praxi', '.press', '.prime', '.pro', '.aaa.pro', '.aca.pro', '.acct.pro', '.arc.pro', '.avocat.pro', '.bar.pro', '.bus.pro', '.chi.pro', '.chiro.pro', '.cpa.pro', '.den.pro', '.dent.pro', '.eng.pro', '.jur.pro', '.law.pro', '.med.pro', '.min.pro', '.nur.pro', '.nurse.pro', '.pharma.pro', '.prof.pro', '.prx.pro', '.recht.pro', '.rel.pro', '.teach.pro', '.vet.pro', '.prod', '.productions', '.prof', '.progressive', '.promo', '.properties', '.property', '.protection', '.pru', '.prudential', '.ps', '.com.ps', '.net.ps', '.org.ps', '.pt', '.co.pt', '.com.pt', '.edu.pt', '.org.pt', '.pub', '.pw', '.pwc', '.py', '.com.py', '.coop.py', '.edu.py', '.mil.py', '.net.py', '.org.py', '.qa', '.com.qa', '.net.qa', '.qpon', '.quebec', '.quest', '.qvc', '.racing', '.radio', '.raid', '.re', '.read', '.realestate', '.realtor', '.realty', '.recipes', '.red', '.redstone', '.redumbrella', '.rehab', '.reise', '.reisen', '.reit', '.reliance', '.ren', '.rent', '.rentals', '.repair', '.report', '.republican', '.rest', '.restaurant', '.review', '.reviews', '.rexroth', '.rich', '.richardli', '.ricoh', '.rightathome', '.ril', '.rio', '.rip', '.rmit', '.ro', '.arts.ro', '.co.ro', '.com.ro', '.firm.ro', '.info.ro', '.ne.ro', '.nom.ro', '.nt.ro', '.or.ro', '.org.ro', '.rec.ro', '.sa.ro', '.srl.ro', '.store.ro', '.tm.ro', '.www.ro', '.rocher', '.rocks', '.rodeo', '.rogers', '.room', '.rs', '.co.rs', '.edu.rs', '.in.rs', '.org.rs', '.rsvp', '.ru', '.adygeya.ru', '.bashkiria.ru', '.bir.ru', '.cbg.ru', '.com.ru', '.dagestan.ru', '.grozny.ru', '.kalmykia.ru', '.kustanai.ru', '.marine.ru', '.mordovia.ru', '.msk.ru', '.mytis.ru', '.nalchik.ru', '.net.ru', '.nov.ru', '.org.ru', '.pp.ru', '.pyatigorsk.ru', '.spb.ru', '.vladikavkaz.ru', '.vladimir.ru', '.rugby', '.ruhr', '.run', '.rw', '.ac.rw', '.co.rw', '.net.rw', '.org.rw', '.rwe', '.ryukyu', '.sa', '.com.sa', '.med.sa', '.saarland', '.safe', '.safety', '.sakura', '.sale', '.salon', '.samsclub', '.samsung', '.sandvik', '.sandvikcoromant', '.sanofi', '.sap', '.sapo', '.sarl', '.sas', '.save', '.saxo', '.sb', '.com.sb', '.net.sb', '.org.sb', '.sbi', '.sbs', '.sc', '.com.sc', '.net.sc', '.org.sc', '.sca', '.scb', '.schaeffler', '.schmidt', '.scholarships', '.school', '.schule', '.schwarz', '.science', '.scjohnson', '.scor', '.scot', '.sd', '.com.sd', '.info.sd', '.net.sd', '.se', '.com.se', '.tm.se', '.search', '.seat', '.secure', '.security', '.seek', '.select', '.sener', '.services', '.ses', '.seven', '.sew', '.sex', '.sexy', '.sfr', '.sg', '.com.sg', '.edu.sg', '.net.sg', '.org.sg', '.per.sg', '.sh', '.shangrila', '.sharp', '.shaw', '.shell', '.shia', '.shiksha', '.shoes', '.shop', '.shopping', '.shouji', '.show', '.showtime', '.shriram', '.si', '.ae.si', '.at.si', '.cn.si', '.co.si', '.de.si', '.uk.si', '.us.si', '.silk', '.sina', '.singles', '.site', '.sj', '.sk', '.ski', '.skin', '.sky', '.skype', '.sl', '.com.sl', '.edu.sl', '.net.sl', '.org.sl', '.sling', '.sm', '.smart', '.smile', '.sn', '.art.sn', '.com.sn', '.edu.sn', '.org.sn', '.perso.sn', '.univ.sn', '.sncf', '.so', '.com.so', '.net.so', '.org.so', '.soccer', '.social', '.softbank', '.software', '.sohu', '.solar', '.solutions', '.song', '.sony', '.soy', '.space', '.spiegel', '.sport', '.spot', '.spreadbetting', '.sr', '.srl', '.srt', '.ss', '.st', '.stada', '.staples', '.star', '.starhub', '.statebank', '.statefarm', '.statoil', '.stc', '.stcgroup', '.stockholm', '.storage', '.store', '.stream', '.studio', '.study', '.style', '.su', '.abkhazia.su', '.adygeya.su', '.aktyubinsk.su', '.arkhangelsk.su', '.armenia.su', '.ashgabad.su', '.azerbaijan.su', '.balashov.su', '.bashkiria.su', '.bryansk.su', '.bukhara.su', '.chimkent.su', '.dagestan.su', '.east-kazakhstan.su', '.exnet.su', '.georgia.su', '.grozny.su', '.ivanovo.su', '.jambyl.su', '.kalmykia.su', '.kaluga.su', '.karacol.su', '.karaganda.su', '.karelia.su', '.khakassia.su', '.krasnodar.su', '.kurgan.su', '.kustanai.su', '.lenug.su', '.mangyshlak.su', '.mordovia.su', '.msk.su', '.murmansk.su', '.nalchik.su', '.navoi.su', '.north-kazakhstan.su', '.nov.su', '.obninsk.su', '.penza.su', '.pokrovsk.su', '.sochi.su', '.spb.su', '.tashkent.su', '.termez.su', '.togliatti.su', '.troitsk.su', '.tselinograd.su', '.tula.su', '.tuva.su', '.vladikavkaz.su', '.vladimir.su', '.vologda.su', '.sucks', '.supplies', '.supply', '.support', '.surf', '.surgery', '.suzuki', '.sv', '.com.sv', '.swatch', '.swiftcover', '.swiss', '.sx', '.sy', '.sydney', '.symantec', '.systems', '.sz', '.co.sz', '.org.sz', '.tab', '.taipei', '.talk', '.taobao', '.target', '.tatamotors', '.tatar', '.tattoo', '.tax', '.taxi', '.tc', '.com.tc', '.net.tc', '.org.tc', '.pro.tc', '.tci', '.td', '.com.td', '.net.td', '.org.td', '.tourism.td', '.tdk', '.team', '.tech', '.technology', '.tel', '.telecity', '.telefonica', '.temasek', '.tennis', '.teva', '.tf', '.tg', '.th', '.ac.th', '.co.th', '.in.th', '.or.th', '.thd', '.theater', '.theatre', '.tiaa', '.tickets', '.tienda', '.tiffany', '.tips', '.tires', '.tirol', '.tj', '.ac.tj', '.aero.tj', '.biz.tj', '.co.tj', '.com.tj', '.coop.tj', '.dyn.tj', '.go.tj', '.info.tj', '.int.tj', '.mil.tj', '.museum.tj', '.my.tj', '.name.tj', '.net.tj', '.org.tj', '.per.tj', '.pro.tj', '.web.tj', '.tjmaxx', '.tjx', '.tk', '.tkmaxx', '.tl', '.com.tl', '.net.tl', '.org.tl', '.tm', '.tmall', '.tn', '.agrinet.tn', '.com.tn', '.defense.tn', '.edunet.tn', '.ens.tn', '.fin.tn', '.ind.tn', '.info.tn', '.intl.tn', '.nat.tn', '.net.tn', '.org.tn', '.perso.tn', '.rnrt.tn', '.rns.tn', '.rnu.tn', '.tourism.tn', '.to', '.today', '.tokyo', '.tools', '.top', '.toray', '.toshiba', '.total', '.tours', '.town', '.toyota', '.toys', '.tp', '.tr', '.av.tr', '.bbs.tr', '.biz.tr', '.com.tr', '.dr.tr', '.gen.tr', '.info.tr', '.name.tr', '.net.tr', '.org.tr', '.tel.tr', '.tv.tr', '.web.tr', '.trade', '.trading', '.training', '.travel', '.travelchannel', '.travelers', '.travelersinsurance', '.trust', '.trv', '.tt', '.biz.tt', '.co.tt', '.com.tt', '.info.tt', '.name.tt', '.net.tt', '.org.tt', '.pro.tt', '.tube', '.tui', '.tunes', '.tushu', '.tv', '.tvs', '.tw', '.club.tw', '.com.tw', '.ebiz.tw', '.edu.tw', '.game.tw', '.gov.tw', '.idv.tw', '.mil.tw', '.net.tw', '.org.tw', '.tz', '.ac.tz', '.co.tz', '.hotel.tz', '.info.tz', '.me.tz', '.mobi.tz', '.ne.tz', '.or.tz', '.sc.tz', '.tv.tz', '.ua', '.biz.ua', '.cherkassy.ua', '.cherkasy.ua', '.chernigov.ua', '.chernivtsi.ua', '.chernovtsy.ua', '.ck.ua', '.cn.ua', '.co.ua', '.com.ua', '.crimea.ua', '.cv.ua', '.dn.ua', '.dnepropetrovsk.ua', '.dnipropetrovsk.ua', '.donetsk.ua', '.dp.ua', '.edu.ua', '.gov.ua', '.if.ua', '.in.ua', '.ivano-frankivsk.ua', '.kh.ua', '.kharkiv.ua', '.kharkov.ua', '.kherson.ua', '.khmelnitskiy.ua', '.kiev.ua', '.kirovograd.ua', '.km.ua', '.kr.ua', '.ks.ua', '.kyiv.ua', '.lg.ua', '.lt.ua', '.lugansk.ua', '.lutsk.ua', '.lviv.ua', '.mk.ua', '.net.ua', '.nikolaev.ua', '.od.ua', '.odesa.ua', '.odessa.ua', '.org.ua', '.pl.ua', '.poltava.ua', '.pp.ua', '.rivne.ua', '.rovno.ua', '.rv.ua', '.sebastopol.ua', '.sm.ua', '.sumy.ua', '.te.ua', '.ternopil.ua', '.uz.ua', '.uzhgorod.ua', '.vinnica.ua', '.vn.ua', '.volyn.ua', '.yalta.ua', '.zaporizhzhe.ua', '.zhitomir.ua', '.zp.ua', '.zt.ua', '.ubank', '.ubs', '.uconnect', '.ug', '.ac.ug', '.co.ug', '.com.ug', '.go.ug', '.ne.ug', '.or.ug', '.org.ug', '.sc.ug', '.uk', '.ac.uk', '.co.uk', '.gov.uk', '.ltd.uk', '.me.uk', '.net.uk', '.org.uk', '.plc.uk', '.sch.uk', '.um', '.unicom', '.university', '.uno', '.uol', '.ups', '.us', '.uy', '.com.uy', '.net.uy', '.org.uy', '.uz', '.biz.uz', '.co.uz', '.com.uz', '.net.uz', '.org.uz', '.va', '.vacations', '.vana', '.vanguard', '.vc', '.com.vc', '.net.vc', '.org.vc', '.ve', '.co.ve', '.com.ve', '.info.ve', '.net.ve', '.org.ve', '.web.ve', '.vegas', '.ventures', '.verisign', '.vermögensberater', '.vermögensberatung', '.versicherung', '.vet', '.vg', '.vi', '.co.vi', '.com.vi', '.k12.vi', '.net.vi', '.org.vi', '.viajes', '.video', '.vig', '.viking', '.villas', '.vin', '.vip', '.virgin', '.visa', '.vision', '.vista', '.vistaprint', '.viva', '.vivo', '.vlaanderen', '.vn', '.ac.vn', '.biz.vn', '.com.vn', '.edu.vn', '.health.vn', '.info.vn', '.int.vn', '.name.vn', '.net.vn', '.org.vn', '.pro.vn', '.vodka', '.volkswagen', '.volvo', '.vote', '.voting', '.voto', '.voyage', '.vu', '.com.vu', '.net.vu', '.org.vu', '.vuelos', '.wales', '.walmart', '.walter', '.wang', '.wanggou', '.warman', '.watch', '.watches', '.weather', '.weatherchannel', '.webcam', '.weber', '.website', '.wed', '.wedding', '.weibo', '.weir', '.wf', '.whoswho', '.wien', '.wiki', '.williamhill', '.win', '.windows', '.wine', '.winners', '.wme', '.wolterskluwer', '.woodside', '.work', '.works', '.world', '.wow', '.ws', '.com.ws', '.net.ws', '.org.ws', '.wtc', '.wtf', '.xbox', '.xerox', '.xfinity', '.xihuan', '.xin', '.xperia', '.xxx', '.xyz', '.yachts', '.yahoo', '.yamaxun', '.yandex', '.ye', '.com.ye', '.net.ye', '.org.ye', '.yodobashi', '.yoga', '.yokohama', '.you', '.youtube', '.yt', '.yun', '.za', '.co.za', '.net.za', '.org.za', '.web.za', '.zappos', '.zara', '.zero', '.zip', '.zippo', '.zm', '.co.zm', '.com.zm', '.org.zm', '.zone', '.zuerich', '.zw', '.co.zw'],

'general':['.com', '.net', '.org', '.info', '.biz', '.cn.com', '.mobi', '.us.com', '.co.com', '.uk.com', '.br.com', '.eu.com', '.za.com', '.ru.com', '.sa.com', '.jpn.com', '.gr.com', '.de.com', '.se.net', '.us.org', '.uk.net', '.ae.org', '.mex.com', '.in.net', '.gb.net', '.jp.net', '.africa.com', '.hu.net', '.qc.com', '.se.com', '.hu.com', '.no.com', '.uy.com', '.gb.com', '.hk.com', '.ar.com', '.kr.com', '.hk.org', '.pty-ltd.com', '.ae.com', '.auz.biz', '.auz.net', '.auz.info', '.nv.com', '.ru.net'],

'internet':['.io', '.online', '.tech', '.download', '.site', '.cloud', '.network', '.it', '.email', '.website', '.blog', '.digital', '.host', '.link', '.stream', '.technology', '.webcam', '.wiki', '.directory', '.systems', '.codes', '.games', '.click', '.computer'],

'finance':['.trade', '.marketing', '.money', '.market', '.cheap', '.loan', '.gold', '.credit', '.investments', '.ventures', '.cash', '.finance', '.financial', '.estate', '.capital', '.tax', '.fund', '.claims', '.mortgage', '.exchange', '.gratis', '.creditcard', '.discount', '.holdings', '.green'],

'technology':['.ai', '.tech', '.app', '.science', '.network', '.it', '.digital', '.technology', '.systems', '.codes', '.computer', '.software', '.energy', '.tel', '.solar', '.security', '.移动', '.industries', '.data', '.te.it', '.ss.it', '.com.ai', '.mi.it', '.co.it'],

'professional':['.pro', '.work', '.consulting', '.expert', '.engineering', '.vet', '.accountants', '.actor', '.accountant', '.associates', '.engineer', '.careers', '.builders', '.attorney', '.doctor', '.management', '.legal', '.lawyer', '.build', '.dentist', '.archi', '.ceo', '.law', '.plumbing', '.jobs'],

'government':['.tax', '.army', '.republican', '.airforce', '.democrat', '.vote', '.voto', '.voting', '.navy', '.int', '.gov', '.gop', '.post', '.mil', '.政府', '.政务'],

'countrycode':['.ac', '.ad', '.ae', '.af', '.ag', '.ai', '.al', '.am', '.ge', '.gf', '.gg', '.gh', '.gi', '.gl', '.gm', '.gn', '.gp', '.gq', '.gr', '.gs', '.gt', '.gu', '.gw', '.gy', '.hk', '.hm', '.hn', '.hr', '.ht', '.hu', '.id', '.ie', '.il', '.im', '.in', '.io', '.iq', '.ir', '.is', '.it', '.je', '.jm', '.jo', '.jp', '.ke', '.kg', '.kh', '.ki', '.km', '.kn', '.kp', '.kr', '.kw', '.ky', '.kz', '.la', '.lb', '.lc', '.li', '.lk', '.lr', '.ls', '.lt', '.lu', '.lv', '.ly', '.ma', '.mc', '.md', '.me', '.mf', '.mg', '.mh', '.mk', '.ml', '.mm', '.mn', '.mo', '.mp', '.mq', '.mr', '.ms', '.mt', '.mu', '.mv', '.mw', '.mx', '.my', '.mz', '.na', '.nc', '.ne', '.nf', '.ng', '.ni', '.nl', '.no', '.np', '.nr', '.nu', '.nz', '.om', '.pa', '.pe', '.pf', '.pg', '.ph', '.pk', '.pl', '.pm', '.pn', '.pr', '.ps', '.pt', '.pw', '.py', '.qa', '.re', '.ro', '.rs', '.ru', '.rw', '.sa', '.sb', '.sc', '.sd', '.se', '.sg', '.sh', '.si', '.sj', '.sk', '.sl', '.sm', '.sn', '.so', '.sr', '.ss', '.st', '.su', '.sv', '.sx', '.sy', '.sz', '.tc', '.td', '.tf', '.tg', '.th', '.tj', '.tk', '.tl', '.tm', '.tn', '.to', '.tp', '.tr', '.tt', '.tv', '.tw', '.tz', '.ua', '.ug', '.uk', '.um', '.us', '.uy', '.uz', '.va', '.vc', '.ve', '.vg', '.vi', '.vn', '.vu', '.wf', '.ws']
}

def getTlds(choice):
	if choice == 1:
		return tldList['countrycode']
	elif choice == 2:
		return tldList['general']
	elif choice == 3:
		return tldList['internet']
	elif choice == 4:
		return tldList['finance']
	elif choice == 5:
		return tldList['technology']
	elif choice == 6:
		return tldList['professional']
	elif choice == 7:
		return tldList['government']
	elif choice == 8:
		return tldList['all']
