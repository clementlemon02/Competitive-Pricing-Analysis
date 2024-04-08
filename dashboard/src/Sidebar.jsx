import React from 'react'
import 
{BsFillDiagram3Fill, BsCoin, BsAirplaneFill, BsPeopleFill, BsBarChartSteps}
 from 'react-icons/bs'

function Sidebar({openSidebarToggle, OpenSidebar}) {
  return (
    <aside id="sidebar" className={openSidebarToggle ? "sidebar-responsive": ""}>
        <div className='sidebar-title'>
            <div className='sidebar-brand'>
                Dashboards
            </div>
            <span className='icon close_icon' onClick={OpenSidebar}>X</span>
        </div>

        <ul className='sidebar-list'>
        <li className='sidebar-list-item'>
                <a href="">
                    <BsFillDiagram3Fill className='icon'/> Price Simulation Model
                </a>
            </li>
            <li className='sidebar-list-item'>
                <a href="">
                <BsCoin className='icon'/> Revenue
                </a>
            </li>
            <li className='sidebar-list-item'>
                <a href="">
                    <BsAirplaneFill className='icon'/> Tourism
                </a>
            </li>
            <li className='sidebar-list-item'>
                <a href="">
                    <BsPeopleFill className='icon'/> Occupancy Rate
                </a>
            </li>
            <li className='sidebar-list-item'>
                <a href="">
                    <BsBarChartSteps className='icon'/> Competitor Pricings
                </a>
            </li>
        </ul>
    </aside>
  )
}

export default Sidebar