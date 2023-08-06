#!/bin/bash

IcmBriefDescription="BISOS Provisioning -- Create the needed framework for BISOS."

####+BEGINNOT: bx:dblock:global:file-insert :file "tools/common/lib/bash/mainRepoRootDetermine.bash"
#
# DO NOT EDIT THIS SECTION (dblock)

# 

scriptSrcRunBase="$( dirname ${BASH_SOURCE[0]} )"
icmPkgRunBase=$(readlink -f ${scriptSrcRunBase}) 
icmSeedFile="${icmPkgRunBase}/seedIcmStandalone.bash"

if [ "${loadFiles}" == "" ] ; then
    "${icmSeedFile}" -l $0 "$@" 
    exit $?
fi

####+END:



function vis_describe {  cat  << _EOF_
BISOS Provisioer is a minimal standaloneIcm that creates a self-reliantIcmEnv
and invokes facilities there.
_EOF_
		      }

# Import Libraries

beSilent="false"
baseDirDefault="/opt/bisosProvisioner"
baseDir=""       # ICM Parameter


function vis_rootDirProvisionersGet {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
Returns one of:
	- baseDir if specified as ICM Parameter on command-line
	- rootDir_provisioners of bx-platformInfoManage.py if it exists
	- default value of baseDirDefault="/opt/bisosProvisioner"
in that order.
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    local bx_platformInfoManage=$( which -a bx-platformInfoManage.py | grep -v venv | head -1 )
    local rootDir_provisioners=""


    if [ -z "${baseDir}" ] ; then    # baseDir as specified as ICM Parameter on command-line
	# Not specified on command-line
	if [ -f "${bx_platformInfoManage}" ] ; then
	    rootDir_provisioners=$( ${bx_platformInfoManage} -i pkgInfoParsGet | grep rootDir_provisioners | cut -d '=' -f 2 )

	    if [ -z "${rootDir_provisioners}" ] ; then
		EH_problem "Missing specified rootDir_provisioners in ${bx_platformInfoManage}"
	    fi
	else
	    rootDir_provisioners=${baseDirDefault}   # 
	fi
    else
	rootDir_provisioners=${baseDir}  # As specified as ICM Parameter on command-line
    fi

    echo "${rootDir_provisioners}"
}

provisionersBase=""

function G_postParamHook {

    provisionersBase="$( vis_rootDirProvisionersGet )"    
    
    # /opt/bisosProvisioner/gitRepos/provisioners/bin/bisosProvisioners_lib.sh
    bisosProvisionersLib="${provisionersBase}/gitRepos/provisioners/bin/bisosProvisioners_lib.sh"

    if [ -f "${bisosProvisionersLib}" ] ; then
	source "${bisosProvisionersLib}"
	#
	# ${bisosProvisionersLib} in turn and in due course
	# sources /bisos/core/bsip/bin/bsipProvision_lib.sh
    fi
}

function vis_examples {
    typeset extraInfo="-h -v -n showRun"
    #typeset extraInfo=""
    typeset runInfo="-p ri=lsipusr:passive"

    typeset examplesInfo="${extraInfo} ${runInfo}"

    visLibExamplesOutput ${G_myName} 
    cat  << _EOF_
$( examplesSeperatorTopLabel "${G_myName}" )
$( examplesSeperatorChapter "BISOS Provisioning:: Standalone ICM Sets Up Selfcontained ICMs" )
$( examplesSeperatorSection "Ensure That Git Is In Place" )
${G_myName} ${extraInfo} -i gitBinsPrep
${G_myName} ${extraInfo} -i gitPrep
$( examplesSeperatorSection "Create bisosProvision base directories" )
${G_myName} ${extraInfo} -p baseDir=/opt/bisosProvisioner -i provisionerRepoClone
${G_myName} ${extraInfo} -p baseDir=/opt/bisosProvisioner -i provisionerBasesPrep
${G_myName} ${extraInfo} -i provisionerRepoClone
${G_myName} ${extraInfo} -i provisionersBasesPrep   # Notable Action -- runs gitPrep + provisionerRepoClone
_EOF_
    
    if [ -f "${bisosProvisionersLib}" ] ; then
	vis_provisionersExamples "${extraInfo}"
    fi
    
    cat  << _EOF_
$( examplesSeperatorChapter "Base BISOS Platform:: Create the Base BISOS Platform" )
$( examplesSeperatorSection "Primary Action -- runs from provisionersBin and from bsip/bin" )
${G_myName} ${extraInfo} -i sysBasePlatform   # Minimal Host or Guest plus Blee
_EOF_
    
}

noArgsHook() {
  vis_examples
}

function modulePrep {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    #provisionersBase="$( vis_rootDirProvisionersGet )"
    
    lpReturn
}


function vis_gitBinsPrep {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    opDo sudo apt-get update
    opDo sudo apt-get -y install git      

    lpReturn
}


function vis_gitPrep {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    #opDo sudo git init

    lpReturn
}



function vis_provisionerRepoClone {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    opDo modulePrep

    # /opt/bisosProvisioner/gitRepos/provisioners
    local provisionersGitBase="${provisionersBase}/gitRepos/provisioners"

    if [ -d "${provisionersGitBase}" ] ; then
	if [ "${beSilent}" != "true" ] ; then  
	    ANT_raw "W: ${provisionersGitBase} is in place, cloning skipped"
	fi
	lpReturn
    fi

    local currentUser=$(id -nu)
    local currentGroup=$(id -ng)
    
    lpDo sudo  mkdir -p "${provisionersBase}"

    lpDo sudo chown ${currentUser}:${currentGroup} "${provisionersBase}"

    local gitReposAnonBase="${provisionersBase}/gitReposAnon"
    local gitReposBase="${provisionersBase}/gitRepos"    
    
    lpDo mkdir -p "${gitReposAnonBase}"
    
    inBaseDirDo "${gitReposAnonBase}" git clone https://github.com/bxGenesis/provisioners.git

    lpDo mkdir -p "${gitReposBase}"

    lpDo ln -s "${gitReposAnonBase}/provisioners" "${gitReposBase}"
    
    lpReturn
}


function vis_provisionersBasesPrep {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    modulePrep

    # /opt/bisosProvisioner/gitRepos/provisioners
    local provisionersGitBase="${provisionersBase}/gitRepos/provisioners"

    if [ -d "${provisionersGitBase}" ] ; then
	if [ "${beSilent}" != "true" ] ; then  
	    ANT_raw "W: ${provisionersGitBase} is in place, preparation skipped"
	fi
	lpReturn
    fi
    
    lpDo vis_gitBinsPrep
    
    lpDo vis_gitPrep
    
    lpDo vis_provisionerRepoClone
    
    lpReturn
}


function vis_sysBasePlatform {
    G_funcEntry
    function describeF {  G_funcEntryShow; cat  << _EOF_
_EOF_
    }
    EH_assert [[ $# -eq 0 ]]

    modulePrep

    lpDo vis_provisionersBasesPrep

    if [ -f "${bisosProvisionersLib}" ] ; then
	source "${bisosProvisionersLib}"
    else
	EH_problem "Missing ${bisosProvisionersLib} -- Aborting"
	lpReturn
    fi
    
    lpDo vis_provisioners_sysBasePlatform
    #
    # vis_provisioners_baseBisosPlatform in turn and in due course
    # runs vis_bsipProvision_baseBisosPlatform
    # from /bisos/core/bsip/bin/bsipProvision_lib.sh
}

